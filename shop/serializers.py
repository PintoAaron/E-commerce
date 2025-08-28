from random import randint

from rest_framework import serializers
from django.db import transaction
from .models import Product,Collection,Cart,CartItem,Review,Customer,Order,OrderItem,ProductImage, MobilePaymentWallet, Address, FavoriteProduct
from .signals import order_created_signal
from .uploader import upload_image
from core.serializers import UserSerializer
from .utils.phone_number import format_phone_number
from .utils.redis import otp_manager
from .utils.sms import send_otp_sms


class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Collection
        fields = ['id','title','product_count','icon','color','background_color']


class UpdateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title','icon','color','background_color']

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id = product_id,**validated_data)
    class Meta:
        model = ProductImage
        fields = ['id','image_url']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)
    collection = CollectionSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id','title','inventory','unit_price','collection','images', 'last_update', 'slug', 'description','user', 'is_active']
        

class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'inventory', 'unit_price', 'collection', 'description', 'is_active']


class CreateProductSerializer(serializers.ModelSerializer):
    image_uploads = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True
    )

    def create(self, validated_data):
        image_uploads = validated_data.pop('image_uploads', [])
        
        user_id = self.context.get('user_id')
        
        product = Product.objects.create(**validated_data, user_id=user_id)
        image_urls = upload_image(image_uploads)
        ProductImage.objects.bulk_create(
            ProductImage(product=product, image_url=image_url) for image_url in image_urls
        )
        return product
    class Meta:
        model = Product
        fields = ['id','title','inventory','unit_price','collection','description','image_uploads']


class SimpleProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['id','title','unit_price','images']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']
    
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self,obj):
        return obj.quantity * obj.product.unit_price
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','created_at','items','total_price']
        
    id = serializers.StringRelatedField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()
    
    
    def get_total_price(self,obj):
        return sum([ item.quantity * item.product.unit_price for item in obj.items.all() ])
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','author','description','date']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id, **validated_data)
    
    


class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']
        
    
    def validate_product_id(self,value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('No product with the given id was found')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id,product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        
        return self.instance
    
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
    
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','membership','birth_date','phone','user','date_joined']



class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'gps', 'apartment', 'landmark']
        
    def save(self, **kwargs):
        customer_id = self.context['customer_id']
        self.instance = Address.objects.create(customer_id=customer_id, **self.validated_data)
        return self.instance
    
    

        
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','quantity','unit_price','product']
    
    

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    shipping_address_id = serializers.IntegerField()
    payment_wallet_id = serializers.IntegerField(required=False, allow_null=True)
    
    
    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('No cart with the given id was found')
        elif CartItem.objects.filter(cart_id = cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id 


    def validate_shipping_address_id(self, shipping_address_id):
        user_id = self.context['user_id']
        customer = Customer.objects.get(user_id=user_id)
        if not Address.objects.filter(pk=shipping_address_id, customer_id=customer.id).exists():
            raise serializers.ValidationError('No address was found')
        return shipping_address_id
    
    
    def validate_payment_wallet_id(self, payment_wallet_id):
        if payment_wallet_id:
            user_id = self.context['user_id']
            customer = Customer.objects.get(user_id=user_id)
            if not MobilePaymentWallet.objects.filter(pk=payment_wallet_id, customer_id=customer.id).exists():
                raise serializers.ValidationError('No payment wallet was found')
        return payment_wallet_id

    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context['user_id']
            cart_id = self.validated_data['cart_id']
            shipping_address_id = self.validated_data['shipping_address_id']
            payment_wallet_id = self.validated_data.get('payment_wallet_id')

            customer = Customer.objects.get(user_id = user_id)
            order = Order.objects.create(customer_id = customer.id, shipping_address_id = shipping_address_id, payment_wallet_id = payment_wallet_id)
            cart_items = CartItem.objects.select_related('product').filter(cart_id = cart_id)
            oder_items = [
            OrderItem(order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity
                    ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(oder_items)
            
            Cart.objects.filter(id = cart_id).delete()
            
            order_created_signal.send_robust(self.__class__,order = order)
                        
            return order
        
        
    



class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status','status']



class MobilePaymentWalletSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    service_provider = serializers.ChoiceField(choices=MobilePaymentWallet.SERVICE_PROVIDERS)
    verified = serializers.BooleanField(read_only=True)
    class Meta:
        model = MobilePaymentWallet
        fields = ['id', 'title', 'service_provider', 'phone_number', 'verified']
        
    
    def validate_phone_number(self, phone_number):
        customer_id = self.context.get('customer_id')
        if MobilePaymentWallet.objects.filter(phone_number=phone_number, customer_id=customer_id).exists():
            raise serializers.ValidationError('A wallet with this phone number already exists for this customer.')
        return format_phone_number(phone_number)
        

    def save(self, **kwargs):
        customer_id = self.context['customer_id']
        self.instance =  MobilePaymentWallet.objects.create(customer_id=customer_id, **self.validated_data)
        otp = randint(100000, 999999)
        send_otp_sms('+233553212010', otp)
        otp_manager.store_otp(self.instance.phone_number, otp)
        return self.instance



class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    orderitems = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer()
    payment_wallet = MobilePaymentWalletSerializer()

    class Meta:
        model = Order
        fields = ['id','customer','payment_status','status','orderitems', 'shipping_address', 'payment_wallet','placed_at']


class VerifyPhoneNumberSerializer(serializers.Serializer):
    otp = serializers.CharField()



class FavoriteProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = SimpleProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['id', 'product', 'created_at', 'product_id']

    def save(self, **kwargs):
        customer_id = self.context['customer_id']
        #create if not exist
        favorite_product, created = FavoriteProduct.objects.get_or_create(
            customer_id=customer_id,
            product_id=self.validated_data['product_id']
        )
        self.instance = favorite_product
        return self.instance
