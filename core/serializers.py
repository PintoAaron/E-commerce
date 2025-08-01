from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth.hashers import make_password
from .models import User


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'phone']

    def save(self, **kwargs):
        email = self.validated_data['email']
        username = self.validated_data.get('username', email.split('@')[0])
        phone = self.validated_data.get('phone', '')
        password = make_password(self.validated_data['password'])
        self.instance = User.objects.create(
            username=username,
            email=email,
            password=password,
            phone=phone,
            is_staff=True
        )
        self.instance.save()
        return self.instance


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'phone','email', 'date_joined']
