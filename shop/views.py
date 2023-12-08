from django.shortcuts import render
from .models import Product,Customer,Order,Collection,OrderItem

def home(request):
    return render(request, 'shop/home.html')