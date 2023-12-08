from django.contrib import admin
from .models import Customer,Collection,Product,Order,OrderItem,Cart,CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'unit_price', 'collection']
    list_select_related = ['collection']
    list_per_page = 10
    list_filter = ['collection']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'phone', 'membership']
    list_editable = ['first_name', 'last_name','phone']
    list_per_page = 10
    list_filter = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'customer']
    list_select_related = ['customer']
    list_per_page = 10
    


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product', 'unit_price', 'quantity',]
    list_select_related = ['order','product']
    list_per_page = 10


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_per_page = 10


