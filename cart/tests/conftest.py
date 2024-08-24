import pytest

from accounts.models import User
from cart.models import Cart
from products.models import Product, Category
from rest_framework.test import APIClient


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
    )


@pytest.fixture
def test_category():
    return Category.objects.create(
        name="test category name",
        description="test category description",
    )


@pytest.fixture
def test_product(test_category, test_user):
    return Product.objects.create(
        name="Test Product",
        price=10.00,
        category=test_category,
        uploaded_by=test_user,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_cart(test_user):
    return Cart.objects.create(user=test_user)
