from unittest.mock import patch

import pytest
from django.core.management import call_command

from apps.accounts.models import User


@pytest.fixture
def mock_send_report():
    with patch("apps.accounts.tasks.send_account_activity_report.delay") as mock:
        yield mock


@pytest.mark.django_db
def test_generate_reports(mock_send_report):
    # Create test users
    User.objects.create(
        username="user1", email="teqwst@gmail.com", is_active=True, receive_reports=True
    )
    User.objects.create(
        username="user2",
        email="tesqwt@gmail.com",
        is_active=True,
        receive_reports=False,
    )
    User.objects.create(
        username="user3",
        email="testwq@gmail.com",
        is_active=False,
        receive_reports=True,
    )

    # Call the custom command
    call_command("generate_reports")

    # Assert that the task was called only for the active user who receives reports
    assert mock_send_report.call_count == 1
    mock_send_report.assert_called_with(User.objects.get(username="user1").id)
