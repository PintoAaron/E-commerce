import pytest
from rest_framework import status
from model_bakery import baker
from shop.models import Collection



@pytest.mark.django_db
class TestCreateCollection():
    def test_if_user_is_anonymous_return_401(self,api_client):
        response = api_client.post('/shop/collections/',{'title':'Fake Collection'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
             
        
    def test_if_user_is_not_staff_return_403(self,api_client,authenticate):
        authenticate()
        response = api_client.post('/shop/collections/',{'title':'Fake Collection'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    def test_if_user_is_staff_and_data_is_valid_return_201(self,api_client,authenticate):
        authenticate(is_staff=True)
        response = api_client.post('/shop/collections/',{'title':'Fake Collection'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Fake Collection'
        
        
    def test_if_user_is_staff_and_data_is_invalid_return_400(self,api_client,authenticate):
        authenticate(is_staff=True)
        response = api_client.post('/shop/collections/',{'title':''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
        
        
@pytest.mark.django_db
class TestRetriveCollection():
    def test_if_collection_exists_return_200(self,api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/shop/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == collection.title
        
    def test_if_collection_does_not_exist_return_404(self,api_client,authenticate):
        authenticate(is_staff=True)
        baker.make(Collection)
        response = api_client.get('/shop/collections/100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        


@pytest.mark.django_db
class TestUpdateCollection():
    def test_if_data_is_valid_return_401(self,api_client,authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = api_client.patch(f'/shop/collections/{collection.id}/',{'title':'Updated Fake Collection'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Fake Collection'
             
        
    def test_if_data_is_invalid_return_400(self,api_client,authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = api_client.patch(f'/shop/collections/{collection.id}/',{'title':''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    
    def test_if_request_method_is_put_return_403(self,api_client,authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = api_client.put(f'/shop/collections/{collection.id}/',{'id':2,'title':'Updated Fake Collection','products_count':1})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        

        
        