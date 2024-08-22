import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

User = get_user_model()


# test_models
@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
    )


# test_views
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def inactive_user(db):
    user = User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
        is_active=False,
    )
    return user


@pytest.fixture
def email_verification_data(inactive_user):
    uid = urlsafe_base64_encode(force_bytes(inactive_user.pk))
    token = default_token_generator.make_token(inactive_user)
    return uid, token
