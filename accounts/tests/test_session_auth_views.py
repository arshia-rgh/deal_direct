import pytest
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils import timezone


@pytest.mark.django_db
class TestSessionListView:
    def test_list_all_session_successfully(self, api_client, active_user):
        api_client.force_authenticate(active_user)

        response = api_client.get(reverse("accounts:session_list"))

        assert response.status_code == 200
        for session in response.data:
            assert "session_key" in session
            assert "expire_date" in session
            assert "last_activity" in session

    def test_list_sessions_unauthorized(self, api_client):
        response = api_client.get(reverse("accounts:session_list"))

        assert response.status_code == 401


@pytest.mark.django_db
class TestSessionLogoutView:
    def test_logout_session_successful(self, api_client, active_user):
        api_client.login(username="testuser", password="testpassword12")

        session = api_client.session
        session.save()

        assert len(Session.objects.all()) == 1

        # check session data
        session_instance = Session.objects.get(session_key=session.session_key)

        session_data = session_instance.get_decoded()

        assert session_data["_auth_user_id"] == "1"
        # end of check session data

        response = api_client.delete(
            reverse("accounts:session_logout", args=(session.session_key,))
        )

        assert response.status_code == 200
        assert response.data["message"] == "Session logged out successfully"

        assert len(Session.objects.all()) == 0

    def test_logout_session_unauthorized(self, api_client):
        response = api_client.delete(
            reverse("accounts:session_logout", args=("fake session key",))
        )

        assert response.status_code == 401

    def test_logout_session_nonexistent_session(self, api_client, active_user):
        api_client.force_authenticate(active_user)

        response = api_client.delete(
            reverse("accounts:session_logout", args=("nonexistent session key",))
        )

        assert response.status_code == 404

    def test_logout_another_user_session(
        self, api_client, active_user, another_active_user
    ):
        api_client.force_authenticate(active_user)

        another_user_session = Session.objects.create(
            session_key="another user session key",
            session_data="",
            expire_date=timezone.now() + timezone.timedelta(days=1),
        )

        another_user_session_data = another_user_session.get_decoded()
        another_user_session_data["_auth_user_id"] = str(another_active_user.id)

        another_user_session.session_data = Session.objects.encode(
            another_user_session_data
        )
        another_user_session.save()

        response = api_client.delete(
            reverse("accounts:session_logout", args=(another_user_session.session_key,))
        )

        assert response.status_code == 403
