from django.urls import path ,include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewSet,basename='orders')

products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
products_router.register('images',viewset=views.ProductImageViewSet,basename='product-images')

carts_router = routers.NestedDefaultRouter(router,'carts',lookup = 'cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items')

orders_router = routers.NestedDefaultRouter(router,'orders',lookup = 'order')
#orders_router.register('items',views.OrderItemViewSet,basename='order-items')

customers_router = routers.NestedDefaultRouter(router,'customers',lookup = 'customer')
customers_router.register('addresses',views.AddressViewSet,basename='customer-addresses')
customers_router.register('mobile-wallets',views.MobilePaymentWalletViewSet,basename='customer-mobile-wallets')
customers_router.register('favorites',views.FavoriteProductViewSet,basename='customer-favorites')

urlpatterns = [

path('',include(router.urls)),
path('',include(products_router.urls)),
path('',include(carts_router.urls)),
path('',include(customers_router.urls)),
    
]