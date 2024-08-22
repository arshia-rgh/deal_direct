import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tasks import send_email_verification_link

User = get_user_model()


class TestUserRegisterView:
    @pytest.mark.django_db
    def test_register_correct_data(self, api_client):
        response = api_client.post(
            reverse("accounts:register"),
            data={
                "username": "testuser",
                "password": "test12pass",
                "email": "test@email.com",
            },
        )
        assert response.status_code == 201
        assert response.data == {
            "message": "User registered successfully, please check your email to active your account"
        }
        assert User.objects.filter(username="testuser").exists()
        assert not User.objects.get(username="testuser").is_active

    @pytest.mark.django_db
    def test_register_missing_fields(self, api_client):
        response = api_client.post(
            reverse("accounts:register"),
            data={"username": "testuser"},
        )
        assert response.status_code == 400
        assert "password" in response.data
        assert "email" in response.data

    @pytest.mark.django_db
    def test_register_existing_username(self, api_client):
        User.objects.create_user(
            username="testuser", email="test1@email.com", password="test12pass"
        )
        response = api_client.post(
            reverse("accounts:register"),
            data={
                "username": "testuser",
                "password": "test12pass",
                "email": "test2@email.com",
            },
        )
        assert response.status_code == 400
        assert "username" in response.data

    @pytest.mark.django_db
    def test_register_invalid_email(self, api_client):
        response = api_client.post(
            reverse("accounts:register"),
            data={
                "username": "testuser",
                "password": "test12pass",
                "email": "invalid-email",
            },
        )
        assert response.status_code == 400
        assert "email" in response.data


class TestVerifyEmailView:
    @pytest.mark.django_db
    def test_email_verification_success(
        self, api_client, inactive_user, email_verification_data
    ):
        uid, token = email_verification_data
        response = api_client.get(
            reverse(
                "accounts:verify_email",
                kwargs={"uidb64": uid, "token": token},
            )
        )
        assert response.status_code == 200
        assert response.data == {
            "message": "Email verified successfully. A bonus will be added to your wallet soon"
        }
        inactive_user.refresh_from_db()
        assert inactive_user.is_active

    @pytest.mark.django_db
    def test_email_verification_invalid_token(
        self, api_client, inactive_user, email_verification_data
    ):
        uid, _ = email_verification_data
        response = api_client.get(
            reverse(
                "accounts:verify_email",
                kwargs={"uidb64": uid, "token": "invalid-token"},
            )
        )
        assert response.status_code == 400
        assert response.data == {"message": "Invalid verification link."}
        inactive_user.refresh_from_db()
        assert not inactive_user.is_active

    @pytest.mark.django_db
    def test_email_verification_invalid_uid(self, api_client, email_verification_data):
        _, token = email_verification_data
        invalid_uid = urlsafe_base64_encode(force_bytes(999))
        response = api_client.get(
            reverse(
                "accounts:verify_email",
                kwargs={"uidb64": invalid_uid, "token": token},
            )
        )
        assert response.status_code == 404


class TestSendMail:
    @pytest.mark.django_db
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_send_mail(self, api_client):
        response = api_client.post(
            reverse("accounts:register"),
            data={
                "username": "testuser",
                "password": "test12pass",
                "email": "test@email.com",
            },
        )
        assert response.status_code == 201

        user = User.objects.get(username="testuser")
        send_email_verification_link(user.id)

        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Verify your email address"
        assert (
            "Please click the link below to verify your email address:"
            in mail.outbox[0].body
        )
        assert mail.outbox[0].to == ["test@email.com"]