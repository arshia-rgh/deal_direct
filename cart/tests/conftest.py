import pytest
from accounts.models import User


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
    )
