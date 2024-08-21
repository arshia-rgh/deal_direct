from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APITestCase

from accounts.tasks import send_email_verification_link

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
    """
    Test case for the Email verification API view.

    This test case includes tests for verifying a user's email with a valid token,
    an invalid token, and an invalid user ID.
    """

    def setUp(self):
        """
        Set up a test user and generate a token for email verification.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="testpassword12",
            is_active=False,
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_email_verification_success(self):
        """
        Test successful email verification.

        This test verifies that a user's email can be successfully verified with a valid token.
        """
        response = self.client.get(
            reverse(
                "accounts:verify_email",
                kwargs={"uidb64": self.uid, "token": self.token},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Email verified successfully."})
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_email_verification_invalid_token(self):
        """
        Test email verification with an invalid token.

        This test verifies that email verification fails with an invalid token.
        """
        response = self.client.get(
            reverse(
                "accounts:verify_email",
                kwargs={"uidb64": self.uid, "token": "invalid-token"},
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message": "Invalid verification link."})
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_email_verification_invalid_uid(self):
        """
        Test email verification with an invalid user ID.

        This test verifies that email verification fails with an invalid user ID.
        """
        invalid_uid = urlsafe_base64_encode(force_bytes(999))
        response = self.client.get(
            reverse(
                "accounts:verify_email",
                kwargs={"uidb64": invalid_uid, "token": self.token},
            )
        )
        self.assertEqual(response.status_code, 404)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class EmailSendTestCase(APITestCase):
    """
    Test case for sending emails.
    """

    def test_send_mail(self):
        """
        Test that an email is sent when a user registers.
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

        # Manually trigger the Celery task for testing purposes
        user = User.objects.get(username="testuser")
        send_email_verification_link(user.id)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Verify your email address")
        self.assertIn(
            "Please click the link below to verify your email address:",
            mail.outbox[0].body,
        )
        self.assertEqual(mail.outbox[0].to, ["test@email.com"])
