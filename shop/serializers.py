from rest_framework import serializers
from django.db import transaction
from .models import Product,Collection,Cart,CartItem,Review,Customer,Order,OrderItem
from .signals import order_created_signal


class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Collection
        fields = ['id','title','product_count']
        
    
class ProductSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Product
        fields = ['id','title','inventory','unit_price','collection']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']        
    

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
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['membership','birth_date','phone','user_id','date_joined']
        
    
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','quantity','unit_price','product']
    
    

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('No cart with the given id was found')
        elif CartItem.objects.filter(cart_id = cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id 
    
    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context['user_id']
            cart_id = self.validated_data['cart_id']
            
            customer = Customer.objects.get(user_id = user_id)
            order = Order.objects.create(customer_id = customer.id)
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
        
        
    

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','customer','payment_status','orderitems']
    


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
