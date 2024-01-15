from rest_framework.test import APIClient
from rest_framework import status

class TestCreateCollection():
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        response = client.post('/shop/collections/',{'title':'product'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED