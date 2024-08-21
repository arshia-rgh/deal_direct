from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class UserModelAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="testpassword12",
        )

    def test_user_creation(self):
        self.assertEqual(self.user1.username, "testuser")
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertTrue(self.user1.check_password("testpassword12"))
