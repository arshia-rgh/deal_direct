from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class UserModelAPITestCase(APITestCase):
    """
    Test case for the User model.

    This test case includes tests for creating, updating, and deleting users,
    as well as handling invalid data during user creation.
    """

    def setUp(self):
        """
        Set up a test user for the test case.

        This method creates a user with predefined username, email, and password.
        """
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="testpassword12",
        )

    def test_user_creation(self):
        """
        Test user creation.

        This test verifies that a user is created with the correct username and password,
        and that the user exists in the database.
        """
        self.assertEqual(self.user1.username, "testuser")
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertTrue(self.user1.check_password("testpassword12"))

    def test_user_creation_invalid_data(self):
        """
        Test user creation with invalid data.

        This test verifies that creating a user with invalid data raises a ValueError.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", email="invalid email", password="")

    def test_user_update(self):
        """
        Test updating user details.

        This test verifies that a user's username can be updated and saved correctly.
        """
        self.user1.username = "updateduser"
        self.user1.save()
        self.assertEqual(self.user1.username, "updateduser")

    def test_user_deletion(self):
        """
        Test deleting a user.

        This test verifies that a user can be deleted and no longer exists in the database.
        """
        user_id = self.user1.id
        self.user1.delete()
        self.assertFalse(User.objects.filter(id=user_id).exists())
