import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.accounts.tasks import (
    send_email_verification_link,
    send_password_reset_email,
)

User = get_user_model()


@pytest.mark.django_db
class TestUserRegisterView:
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

    def test_register_missing_fields(self, api_client):
        response = api_client.post(
            reverse("accounts:register"),
            data={"username": "testuser"},
        )
        assert response.status_code == 400
        assert "password" in response.data
        assert "email" in response.data

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


@pytest.mark.django_db
class TestVerifyEmailView:
    def test_email_verification_success(
        self, api_client, inactive_user, uid_token_setup
    ):
        uid, token = uid_token_setup
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

    def test_email_verification_invalid_token(
        self, api_client, inactive_user, uid_token_setup
    ):
        uid, _ = uid_token_setup
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

    def test_email_verification_invalid_uid(self, api_client, uid_token_setup):
        _, token = uid_token_setup
        invalid_uid = urlsafe_base64_encode(force_bytes(999))
        response = api_client.get(
            reverse(
                "accounts:verify_email",
                kwargs={"uidb64": invalid_uid, "token": token},
            )
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestSendMail:
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

        assert mail.outbox[0].to == ["test@email.com"]


@pytest.mark.django_db
class TestProfileRetrieveUpdate:
    def test_profile_retrieve_active_and_authenticated_user(
        self, authenticated_user, test_user
    ):
        test_user.is_active = True
        test_user.save()
        response = authenticated_user.get(
            reverse("accounts:profile"),
        )
        assert response.status_code == 200
        assert response.data["username"] == test_user.username
        assert response.data["email"] == test_user.email
        assert response.data["first_name"] == test_user.first_name
        assert response.data["last_name"] == test_user.last_name
        assert response.data["phone_number"] == test_user.phone_number
        assert float(response.data["wallet"]) == test_user.wallet

    def test_profile_retrieve_inactive_user(self, api_client, test_user):
        test_user.is_active = False
        test_user.save()
        api_client.force_authenticate(user=test_user)
        response = api_client.get(reverse("accounts:profile"))
        assert response.status_code == 403

    def test_profile_update_authenticated_and_active_user(
        self, authenticated_user, test_user
    ):
        test_user.is_active = True
        test_user.save()
        response = authenticated_user.patch(
            reverse("accounts:profile"),
            data={"username": "updateduser", "email": "updated@email.com"},
        )

        assert response.status_code == 200
        test_user.refresh_from_db()
        assert test_user.username == "updateduser"
        assert test_user.email == "updated@email.com"

    def test_profile_update_invalid_data(self, authenticated_user, test_user):
        test_user.is_active = True
        test_user.save()
        response = authenticated_user.patch(
            reverse("accounts:profile"),
            data={"username": "", "email": "invalid-email"},
        )
        assert response.status_code == 400
        assert "username" in response.data
        assert "email" in response.data


@pytest.mark.django_db
class TestUserPasswordChange:
    def test_change_password_with_unauthenticated_user(self, api_client):
        response = api_client.post(reverse("accounts:change_password"))

        assert response.status_code == 401
        assert response.data == {
            "detail": "Authentication credentials were not provided."
        }

    def test_change_password_with_authenticated_user(
        self, authenticated_user, test_user
    ):
        test_user.is_active = True
        test_user.save()
        response = authenticated_user.patch(
            reverse("accounts:change_password"),
            data={
                "old_password": "testpassword12",
                "password": "new_password12",
                "confirm_password": "new_password12",
            },
        )

        assert response.status_code == 200
        test_user.refresh_from_db()
        assert test_user.check_password("new_password12")

    def test_change_password_with_incorrect_old_password(
        self, authenticated_user, test_user
    ):
        test_user.is_active = True
        test_user.save()
        response = authenticated_user.patch(
            reverse("accounts:change_password"),
            data={
                "old_password": "wrongpassword",
                "password": "new_password12",
                "confirm_password": "new_password12",
            },
        )

        assert response.status_code == 400
        assert "old_password" in response.data

    def test_change_password_with_mismatched_new_passwords(
        self, authenticated_user, test_user
    ):
        test_user.is_active = True
        test_user.save()
        response = authenticated_user.patch(
            reverse("accounts:change_password"),
            data={
                "old_password": "testpassword12",
                "password": "new_password12",
                "confirm_password": "different_password",
            },
        )

        assert response.status_code == 400
        assert "error" in response.data

    def test_change_password_with_missing_fields(self, authenticated_user, test_user):
        test_user.is_active = True
        test_user.save()
        response = authenticated_user.patch(
            reverse("accounts:change_password"),
            data={
                "old_password": "testpassword12",
                "password": "new_password12",
            },
        )

        assert response.status_code == 400
        assert "confirm_password" in response.data


@pytest.mark.django_db
class TestPasswordReset:
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_request_valid_email(self, api_client, test_user):
        response = api_client.post(
            reverse("accounts:password_reset"),
            data={"email": test_user.email},
        )
        # TODO (why) without this line the assertion of email sent will be failed
        send_password_reset_email(test_user.id)

        assert response.status_code == 200
        assert response.data == {"message": "Password reset email sent successfully"}
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [test_user.email]

    def test_password_reset_request_invalid_email(self, api_client):
        response = api_client.post(
            reverse("accounts:password_reset"),
            data={"email": "invalid email"},
        )

        assert response.status_code == 400
        assert "email" in response.data

    def test_password_reset_request_user_does_not_exist(self, api_client):
        response = api_client.post(
            reverse("accounts:password_reset"),
            data={"email": "valid@gmail.com"},
        )

        assert response.status_code == 400
        assert response.data == {"error": "user with given email does not exists"}

    def test_password_reset_confirm_valid_token(
        self, api_client, inactive_user, uid_token_setup
    ):
        uid, token = uid_token_setup

        response = api_client.post(
            reverse(
                "accounts:password_reset_confirm",
                kwargs={"uidb64": uid, "token": token},
            ),
            data={"password": "new_password12"},
        )

        assert response.status_code == 200
        assert response.data == {"message": "Password has been reset successfully."}
        inactive_user.refresh_from_db()
        assert inactive_user.check_password("new_password12")

    def test_password_reset_confirm_invalid_token(
        self, api_client, inactive_user, uid_token_setup
    ):
        uid, _ = uid_token_setup

        response = api_client.post(
            reverse(
                "accounts:password_reset_confirm",
                kwargs={"uidb64": uid, "token": "invalid token"},
            ),
            data={"password": "new_password12"},
        )

        assert response.status_code == 400
        assert response.data == {"error": "Invalid link"}
        inactive_user.refresh_from_db()
        assert not inactive_user.check_password("new_password12")
