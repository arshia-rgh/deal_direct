import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


def test_user_creation(test_user):
    assert test_user.username == "testuser"
    assert User.objects.filter(username="testuser").exists()
    assert test_user.check_password("testpassword12")


def test_user_creation_invalid_data(db):
    with pytest.raises(ValueError):
        User.objects.create_user(username="", email="invalid email", password="")


def test_user_update(test_user):
    test_user.username = "updateduser"
    test_user.save()
    assert test_user.username == "updateduser"


def test_user_deletion(test_user):
    user_id = test_user.id
    test_user.delete()
    assert not User.objects.filter(id=user_id).exists()
