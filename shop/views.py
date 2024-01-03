from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from .models import Product,Collection,OrderItem,Cart,Review,CartItem,Customer
from .serializers import ProductSerializer,CollectionSerializer,CartSerializer,ReviewSerializer,CartItemSerializer,CreateCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter    
    search_fields  = ['title','description']
    ordering_fields = ['unit_price','last_update']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).exists():
            return Response({'error':'Product cannot be deleted because it is associated with an order item'},status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    permission_classes = [IsAdminOrReadOnly]
    
    

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items__product').all()


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]
    
    
    @action(detail = False,methods = ['GET','PUT'],permission_classes = [IsAuthenticated])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id = request.user.id)
        print(customer)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
    
    
