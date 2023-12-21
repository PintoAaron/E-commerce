from django.shortcuts import render
from django.db.models import Count
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Product,Collection,OrderItem
from .serializers import ProductSerializer,CollectionSerializer


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('collection').all()
    
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).exists():
            return Response({'error':'Product cannot be deleted because it is associated with an order item'},status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

class CollectionViewset(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.annotate(product_count=Count('products')).all()