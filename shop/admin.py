from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Customer, Collection, Product, Order, OrderItem, Cart


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['id', 'title', 'unit_price', 'collection', 'inventory', 'inventory_status']
    list_editable = ['inventory']
    list_select_related = ['collection']
    list_per_page = 10
    list_filter = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory > 10:
            return 'In Stock'
        if product.inventory < 10:
            return 'Low Stock'
        return 'Out of Stock'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        queryset.update(inventory=0)
        self.message_user(request, 'Inventory Cleared', messages.SUCCESS)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_filter = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (reverse('admin:shop_order_changelist') + '?' + urlencode({'customer__id': str(customer.id)}))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ['mark_success']
    list_display = ['id', 'placed_at', 'payment_status', 'customer', 'order_items']
    list_select_related = ['customer']
    list_per_page = 10

    @admin.display(ordering='order_items_count')
    def order_items(self, order):
        url = (reverse('admin:shop_orderitem_changelist') + '?' + urlencode({'order__id': str(order.id)}))
        return format_html('<a href="{}">{}</a>', url, order.order_items_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_items_count=Count('orderitem'))

    @admin.action(description='Mark as Complete')
    def mark_success(self, request, queryset):
        updated_count = queryset.update(payment_status='C')
        self.message_user(request, f'{updated_count} order marked as Complete', messages.SUCCESS)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'products_count']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:shop_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)}))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'product', 'unit_price', 'quantity']
    list_select_related = ['order', 'product']
    list_per_page = 10

    def order_id(self, orderitem):
        return orderitem.order.id


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_per_page = 10
