import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from accounts.models import User
from products.models import Product, Category


@pytest.fixture
def test_category():
    return Category.objects.create(
        name="test category name",
        description="test category description",
    )


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="test user",
        password="test password",
        email="testmail@email.com",
    )


@pytest.fixture
def test_product(test_category, test_user):
    image = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
        content_type="image/jpeg",
    )
    return Product.objects.create(
        name="test product name",
        description="test product description",
        price=10.00,
        image=image,
        category=test_category,
        uploaded_by=test_user,
    )


@pytest.fixture
def api_client():
    return APIClient()
