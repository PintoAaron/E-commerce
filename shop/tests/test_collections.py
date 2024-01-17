import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCreateCollection():
    def test_if_user_is_anonymous_return_401(self,api_client,collection):
        response = api_client.post('/shop/collections/',{'title':'Fake Collection 2'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
             
        
    def test_if_user_is_not_staff_return_403(self,api_client,authenticate,collection):
        authenticate()
        response = api_client.post('/shop/collections/',{'title':'Fake Collection 2'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    def test_if_user_is_staff_and_data_is_valid_return_201(self,api_client,authenticate,collection):
        authenticate(is_staff=True)
        response = api_client.post('/shop/collections/',{'title':'Fake Collection 2'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Fake Collection 2'
        
        
    def test_if_user_is_staff_and_data_is_invalid_return_400(self,api_client,authenticate):
        authenticate(is_staff=True)
        response = api_client.post('/shop/collections/',{'title':''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
        
        
@pytest.mark.django_db
class TestRetriveCollection():
    def test_if_user_is_anonymous_returns_200(self,api_client,collection):
        response = api_client.get('/shop/collections/')
        assert response.status_code == status.HTTP_200_OK
        
    def test_if_user_is_staff_return_200(self,api_client,authenticate,collection):
        authenticate(is_staff=True)
        response = api_client.get('/shop/collections/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() and response.json()[0]['title'] == 'Fake Collection'
        


@pytest.mark.django_db
class TestUpdateCollection():
    def test_if_user_is_anonymous_return_401(self,api_client,collection):
        response = api_client.patch('/shop/collections/1/',{'title':'Updated Fake Collection'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
             
        
    def test_if_user_is_not_staff_return_403(self,api_client,authenticate,collection):
        authenticate()
        response = api_client.patch('/shop/collections/1/',{'title':'Updated Fake Collection'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    def test_if_user_is_staff_and_data_is_valid_return_200(self,api_client,authenticate,collection):
        authenticate(is_staff=True)
        response = api_client.patch('/shop/collections/1/',{'title':'Updated Fake Collection'})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == 'Updated Fake Collection'
        
        
    def test_if_user_is_staff_and_data_is_invalid_return_400(self,api_client,authenticate,collection):
        authenticate(is_staff=True)
        response = api_client.patch('/shop/collections/1/',{'title':''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        
        