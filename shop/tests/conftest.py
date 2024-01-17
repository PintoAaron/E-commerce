from django.contrib.auth.models import User
from rest_framework.test import APIClient
from shop.models import Collection, Product
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate


@pytest.fixture
def collection():
    return Collection.objects.create(title='Fake Collection')


@pytest.fixture
def product(collection):
    return Product.objects.create(title="Fake Product", inventory=3, unit_price=4.2, collection=collection)
