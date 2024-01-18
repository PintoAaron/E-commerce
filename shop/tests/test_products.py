import pytest
from rest_framework import status
from model_bakery import baker 
from shop.models import Collection, Product, OrderItem


@pytest.mark.django_db
class TestCreateProduct():
    def test_if_user_is_anonymous_return_401(self, api_client):
        collection = baker.make(Collection)
        response = api_client.post('/shop/products/', {'title': 'Fake Product 2', 'inventory': 1, 'unit_price': 2.5, 'collection': collection.id})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_if_user_is_not_staff_return_403(self, api_client, authenticate):
        authenticate()
        collection = baker.make(Collection)
        response = api_client.post('/shop/products/', {'title': 'Fake Product 2', 'inventory': 1, 'unit_price': 2.5, 'collection': collection.id})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    def test_if_user_is_staff_and_data_is_valid_return_201(self, api_client, authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = api_client.post('/shop/products/', {'title': 'Fake Product 2', 'inventory': 1, 'unit_price': 2.5, 'collection': collection.id})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Fake Product 2' and response.data['collection'] == collection.id
        
        
    def test_if_user_is_staff_and_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = api_client.post('/shop/products/', {'title': '', 'inventory': 1, 'unit_price': 2.5, 'collection': collection.id})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        


@pytest.mark.django_db
class TestRetrieveProduct():
    def test_if_product_exits_return_200(self,api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.get(f'/shop/products/{product.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == product.title and response.json()['collection'] == collection.id
        
    
    def test_if_product_does_not_exist_return_404(self,api_client):
        baker.make(Product)
        response = api_client.get('/shop/products/100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND



@pytest.mark.django_db
class TestUpdateProduct():
    def test_if_data_is_valid_return_200(self,api_client,authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.patch(f'/shop/products/{product.id}/',{'title':'Updated Fake Product'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Fake Product'
        
        
    def test_if_data_is_invalid_return_400(self,api_client,authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.patch(f'/shop/products/{product.id}/',{'title':''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        

    def test_if_user_is_not_staff_return_403(self,api_client,authenticate):
        authenticate()
        product = baker.make(Product)
        response = api_client.patch(f'/shop/products/{product.id}/',{'title':'Updated Fake Product'})
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeleteProduct():
    def test_if_product_exists_return_204(self,api_client,authenticate):
        authenticate(is_staff=True)
        product = baker.make(Product)
        response = api_client.delete(f'/shop/products/{product.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        
    def test_if_product_does_not_exist_return_404(self,api_client,authenticate):
        authenticate(is_staff=True)
        response = api_client.delete(f'/shop/products/1/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_if_product_is_associated_with_an_order_return_405(self,api_client,authenticate):
        authenticate(is_staff=True)
        product = baker.make(Product)
        orderitem = baker.make(OrderItem, product=product)
        response = api_client.delete(f'/shop/products/{product.id}/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data['error'] == 'Product cannot be deleted because it is associated with an order item'