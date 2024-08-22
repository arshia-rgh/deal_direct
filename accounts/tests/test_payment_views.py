from decimal import Decimal

import pytest
from django.urls import reverse

from accounts.tests.conftest import active_user


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
        assert response.url == "http://example.com"

    def test_increase_wallet_invalid_data(self, api_client, active_user):
        api_client.force_authenticate(active_user)

        response = api_client.post(
            reverse("accounts:deposit"),
            data={
                "amount": "invalid amount",
            },
        )

        assert response.status_code == 400

    def test_increase_wallet_payment_fail(
        self, api_client, active_user, mock_send_request
    ):
        mock_send_request.return_value = {"status": False, "code": 500}

        api_client.force_authenticate(active_user)

        response = api_client.post(
            reverse("accounts:deposit"),
            data={
                "amount": "10.00",
            },
        )

        assert response.status_code == 400
        assert response.data["error"] == "Payment request failed"
        assert response.data["code"] == 500

    def test_verify_deposit_success(
        self, mock_update_wallet_balance, mock_verify, api_client, active_user
    ):
        mock_verify.return_value = {"status": True, "RefID": "123456"}

        api_client.force_authenticate(active_user)

        response = api_client.post(
            reverse("accounts:verify-deposit"),
            data={"Authority": "auth123", "Amount": "100.00"},
        )

        assert response.status_code == 200
        assert response.data["status"] == "Payment verified successfully"
        assert response.data["RefID"] == "123456"
        mock_update_wallet_balance.delay.assert_called_once_with(
            active_user.id, "100.00"
        )
