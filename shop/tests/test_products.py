import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCreateProduct():
    def test_if_user_is_anonymous_return_401(self, api_client, collection):
        response = api_client.post(
            '/shop/products/', {'title': 'Fake Product 2', 'inventory': 1, 'unit_price': 2.5, 'collection': collection.id})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_if_user_is_not_staff_return_403(self, api_client, authenticate, collection):
        authenticate()
        response = api_client.post(
            '/shop/products/', {'title': 'Fake Product 2', 'inventory': 1, 'unit_price': 2.5, 'collection': collection.id})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    def test_if_user_is_staff_and_data_is_valid_return_403(self, api_client, authenticate, collection):
        authenticate(is_staff=True)
        response = api_client.post(
            '/shop/products/', {'title': 'Fake Product 2', 'inventory': 1, 'unit_price': 2.5, 'collection': collection.id})
        assert response.status_code == status.HTTP_201_CREATED
        


@pytest.mark.django_db
class TestRetrieveProduct():
    def test_if_user_is_anonymous_return_200(self,api_client,product):
        response = api_client.get('/shop/products/')
        assert response.status_code == status.HTTP_200_OK
