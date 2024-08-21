from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

User = get_user_model()


class UserRegisterViewAPITestCase(APITestCase):
    """
    Test case for the User registration API view.

    This test case includes tests for registering a user with correct data,
    missing fields, existing username, and invalid email format.
    """

    def test_register_correct_data(self):
        """
        Test user registration with correct data.

        This test verifies that a user can be registered with valid data,
        and checks that the user is created but not yet active.
        """
        response = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "testuser",
                "password": "test12pass",
                "email": "test@email.com",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "message": "User registered successfully, please check your email to active your account"
            },
        )
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertFalse(User.objects.get(username="testuser").is_active)

    def test_register_missing_fields(self):
        """
        Test user registration with missing fields.

        This test verifies that the registration fails when required fields are missing,
        and checks that the appropriate error messages are returned.
        """
        response = self.client.post(
            reverse("accounts:register"),
            data={"username": "testuser"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)
        self.assertIn("email", response.data)

    def test_register_existing_username(self):
        """
        Test user registration with an existing username.

        This test verifies that the registration fails when the username already exists,
        and checks that the appropriate error message is returned.
        """
        User.objects.create_user(
            username="testuser", email="test1@email.com", password="test12pass"
        )
        response = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "testuser",
                "password": "test12pass",
                "email": "test2@email.com",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)

    def test_register_invalid_email(self):
        """
        Test user registration with an invalid email format.

        This test verifies that the registration fails when the email format is invalid,
        and checks that the appropriate error message is returned.
        """
        response = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "testuser",
                "password": "test12pass",
                "email": "invalid-email",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)


class EmailVerifyViewAPItestCase(APITestCase):
    pass
