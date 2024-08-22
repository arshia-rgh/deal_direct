import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel:
    """
    Test suite for the User model.
    """

    def test_user_creation(self, test_user):
        """
        Test that a user is created successfully with valid data.
        """
        assert test_user.username == "testuser"
        assert User.objects.filter(username="testuser").exists()
        assert test_user.check_password("testpassword12")

    def test_user_creation_invalid_data(self, db):
        """
        Test that creating a user with invalid data raises a ValueError.
        """
        with pytest.raises(ValueError):
            User.objects.create_user(username="", email="invalid email", password="")

    def test_user_update(self, test_user):
        """
        Test that a user's data can be updated successfully.
        """
        test_user.username = "updateduser"
        test_user.save()
        assert test_user.username == "updateduser"

    def test_user_deletion(self, test_user):
        """
        Test that a user can be deleted successfully.
        """
        user_id = test_user.id
        test_user.delete()
        assert not User.objects.filter(id=user_id).exists()
