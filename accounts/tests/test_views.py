from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

User = get_user_model()


class UserRegisterViewAPITestCase(APITestCase):
    def test_register(self):
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
