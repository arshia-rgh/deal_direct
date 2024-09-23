import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.products.models import Product


@pytest.fixture
def test_product():
    product = baker.make(Product)

    return product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_active_user():
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
        is_active=True,
    )
