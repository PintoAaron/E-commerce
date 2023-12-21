from rest_framework import serializers 
from .models import Product,Collection


class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Collection
        fields = ['id','title','product_count']
        
    
class ProductSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Product
        fields = ['id','title','inventory','unit_price','collection']