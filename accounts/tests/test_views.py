from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

User = get_user_model()


class UserRegisterViewAPITestCase(APITestCase):
    def test_register_correct_data(self):
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
        response = self.client.post(
            reverse("accounts:register"),
            data={"username": "testuser"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)
        self.assertIn("email", response.data)

    def test_register_existing_username(self):
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
