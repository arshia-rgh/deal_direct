import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDeposit:
    def test_increase_wallet_success(self, api_client, active_user, mock_send_request):
        mock_send_request.return_value = {"status": True, "url": "http://example.com"}

        api_client.force_authenticate(active_user)

        response = api_client.post(
            reverse("accounts:deposit"),
            data={"amount": 10.00},
        )
        assert response.status_code == 302
