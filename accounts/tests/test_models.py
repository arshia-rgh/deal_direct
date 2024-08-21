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

    def test_user_creation_invalid_data(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", email="invalid email", password="")

    def test_user_update(self):
        self.user1.username = "updateduser"
        self.user1.save()
        self.assertEqual(self.user1.username, "updateduser")

    def test_user_deletion(self):
        user_id = self.user1.id
        self.user1.delete()
        self.assertFalse(User.objects.filter(id=user_id).exists())
