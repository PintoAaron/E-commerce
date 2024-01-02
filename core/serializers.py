from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    username = serializers.StringRelatedField(read_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','email','password','first_name','last_name']
        
    
    def save(self, **kwargs):
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        
        username = first_name[0].lower() + last_name.lower()
        password = make_password(self.validated_data['password'])
        self.instance = User.objects.create(username = username,email = email, password = password, first_name = first_name, last_name = last_name)
        self.instance.save()
        return self.instance

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','email','first_name','last_name']
        
    

    
    
    