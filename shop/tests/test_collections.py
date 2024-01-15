from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestCreateCollection():
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        response = client.post('/shop/collections/',{'title':'product'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
             
        
    def test_if_user_is_not_staff_return_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post('/shop/collections/',{'title':'product'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    def test_if_user_is_staff_and_data_is_valid_return_201(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/shop/collections/',{'title':'product'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        
        
    def test_if_user_is_staff_and_data_is_invalid_return_400(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/shop/collections/',{'title':''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        