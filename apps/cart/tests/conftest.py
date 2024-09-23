import pytest

from apps.accounts.models import User
from apps.cart.models import Cart
from apps.products.models import Product, Category
from rest_framework.test import APIClient


@pytest.fixture
def test_active_user():
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
        is_active=True,
    )


@pytest.fixture
def test_category():
    return Category.objects.create(
        name="test category name",
        description="test category description",
    )


@pytest.fixture
def test_product(test_category, test_active_user):
    return Product.objects.create(
        name="Test Product",
        price=10.00,
        category=test_category,
        uploaded_by=test_active_user,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_cart(test_active_user):
    return Cart.objects.create(user=test_active_user)


@pytest.fixture
def test_user_2():
    return User.objects.create_user(
        username="testuser 2 ",
        email="test2@gmail.com",
        password="testpassword12",
        is_active=True,
    )


@pytest.fixture
def test_cart_2(test_user_2):
    return Cart.objects.create(
        user=test_user_2,
    )
