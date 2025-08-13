from django.core.validators import MinValueValidator
from django.contrib import admin
from django.conf import settings
from django.db import models
# from uuid import uuid4


class Collection(models.Model):
    title = models.CharField(max_length=100, null=False)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    icon = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    background_color = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(1)])
    description = models.TextField(null=True, blank=True)
    inventory = models.PositiveIntegerField(default=0)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=255, null=True, blank=True)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP = [

        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    phone = models.CharField(max_length=50)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP, default=MEMBERSHIP_BRONZE)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

        permissions = [
            ('view_history', 'Can view history'),
        ]
        


class FavoriteProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['customer', 'product']]


class MobilePaymentWallet(models.Model):
    MTN_SERVICE = 'MTN'
    AIRTEL_SERVICE = 'AIRTEL'
    TELECEL_SERVICE = 'TELECEL'

    SERVICE_PROVIDERS = [
        (MTN_SERVICE, 'MTN'),
        (AIRTEL_SERVICE, 'AIRTEL'),
        (TELECEL_SERVICE, 'TELECEL'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='mobile_wallets')
    title = models.CharField(max_length=100, null=True, blank=True)
    service_provider = models.CharField(max_length=20, choices=SERVICE_PROVIDERS, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    verified = models.BooleanField(default=False)


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100, null=True, blank=True)
    gps = models.CharField(max_length=100, null=True, blank=True)
    apartment = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)


class Order(models.Model):
    ORDER_PENDING = 'P'
    ORDER_FAILED = 'F'
    ORDER_COMPLETED = 'C'

    ORDER = [
        (ORDER_PENDING, 'Pending'),
        (ORDER_FAILED, 'Failed'),
        (ORDER_COMPLETED, 'Completed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=ORDER, default=ORDER_PENDING)

    class Meta:
        ordering = ['-placed_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1)])


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
