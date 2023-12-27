from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

class Collection(models.Model):
    title = models.CharField(max_length=100, null=False)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(1)])
    description = models.TextField(null=True, blank=True)
    inventory = models.PositiveIntegerField(default=0)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    
    class Meta:
        ordering =  ['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP = [

        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP, default=MEMBERSHIP_BRONZE)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    
    class Meta:
        ordering = ['first_name', 'last_name']


class Address(models.Model):
    customer = models.OneToOneField(Customer, primary_key=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)


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
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(1)])

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default = uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField()
    
    
    class Meta:
        unique_together = [['cart','product']]

class Review(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name = 'reviews')
    author = models.CharField(max_length = 255)
    description  = models.TextField()
    date = models.DateField(auto_now_add = True)