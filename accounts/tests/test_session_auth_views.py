import pytest
from django.urls import reverse


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
