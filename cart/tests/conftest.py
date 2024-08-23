import pytest

from accounts.models import User
from products.models import Product, Category


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
