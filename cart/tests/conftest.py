import pytest

from accounts.models import User
from products.models import Product


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
    )


@pytest.fixture
def test_product():
    return Product.objects.create(
        name="Test Product",
        price=10.00,
    )
