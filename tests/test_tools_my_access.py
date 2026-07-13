"""Tests for my_access tools."""

from unittest.mock import patch

import pytest
from britive.exceptions import (
    ApprovalRequiredButNoJustificationProvided,
    ProfileCheckoutAlreadyApproved,
)
from britive.exceptions.badrequest import PendingProfileApprovalRequestError


class TestMyAccessCheckout:
    """Test my_access_checkout tool (asynchronous, non-blocking)."""

    def test_checkout_no_approval_returns_checked_out(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkout

        mock_britive_client.my_access.checkout.return_value = {"transactionId": "tx-123"}

        result = my_access_checkout(profile_id="prof-1", environment_id="env-1")

        # The probe checkout is attempted with justification withheld so approval-required
        # profiles fail fast rather than blocking.
        mock_britive_client.my_access.checkout.assert_called_once_with(
            profile_id="prof-1",
            environment_id="env-1",
            headers=None,
            include_credentials=False,
            justification=None,
            otp=None,
            programmatic=False,
            progress_func=None,
            ticket_id=None,
            ticket_type=None,
        )
        assert result == {"status": "checked_out", "transaction": {"transactionId": "tx-123"}}

    def test_checkout_approval_no_justification_returns_justification_required(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_access import my_access_checkout

        mock_britive_client.my_access.checkout.side_effect = ApprovalRequiredButNoJustificationProvided()

        result = my_access_checkout(profile_id="prof-1", environment_id="env-1")

        assert result["status"] == "justification_required"
        mock_britive_client.my_access.request_approval.assert_not_called()

    def test_checkout_approval_with_justification_returns_pending(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_access import my_access_checkout

        mock_britive_client.my_access.checkout.side_effect = ApprovalRequiredButNoJustificationProvided()
        mock_britive_client.my_access.request_approval.return_value = {"requestId": "req-9"}

        result = my_access_checkout(
            profile_id="prof-1",
            environment_id="env-1",
            justification="Need access for deployment",
            include_credentials=True,
            programmatic=True,
            ticket_id="JIRA-100",
            ticket_type="incident",
        )

        assert result["status"] == "pending_approval"
        assert result["request_id"] == "req-9"
        assert result["profile_id"] == "prof-1"
        assert result["environment_id"] == "env-1"
        assert result["include_credentials"] is True
        assert result["programmatic"] is True
        mock_britive_client.my_access.request_approval.assert_called_once_with(
            profile_id="prof-1",
            justification="Need access for deployment",
            environment_id="env-1",
            block_until_disposition=False,
            ticket_id="JIRA-100",
            ticket_type="incident",
            headers=None,
        )

    def test_checkout_already_pending_returns_pending_approval(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_access import my_access_checkout

        # A request is already outstanding -> the checkout probe raises PendingProfileApprovalRequestError.
        mock_britive_client.my_access.checkout.side_effect = PendingProfileApprovalRequestError()

        result = my_access_checkout(
            profile_id="prof-1", environment_id="env-1", justification="need it"
        )

        assert result["status"] == "pending_approval"
        assert result["request_id"] is None
        # must not resubmit an approval request
        mock_britive_client.my_access.request_approval.assert_not_called()

    def test_checkout_already_approved_race_returns_checked_out(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_access import my_access_checkout

        mock_britive_client.my_access.checkout.side_effect = [
            ApprovalRequiredButNoJustificationProvided(),
            {"transactionId": "tx-777"},
        ]
        mock_britive_client.my_access.request_approval.side_effect = ProfileCheckoutAlreadyApproved()

        result = my_access_checkout(
            profile_id="prof-1", environment_id="env-1", justification="already ok"
        )

        assert result == {"status": "checked_out", "transaction": {"transactionId": "tx-777"}}

    def test_checkout_obo_passes_header(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkout

        mock_britive_client.my_access.checkout.return_value = {"transactionId": "tx-123"}

        my_access_checkout(profile_id="prof-1", environment_id="env-1")

        call_kwargs = mock_britive_client.my_access.checkout.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}

    def test_checkout_obo_passes_header_to_request_approval(
        self, mock_client_wrapper_obo, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_access import my_access_checkout

        mock_britive_client.my_access.checkout.side_effect = ApprovalRequiredButNoJustificationProvided()
        mock_britive_client.my_access.request_approval.return_value = {"requestId": "req-9"}

        my_access_checkout(profile_id="prof-1", environment_id="env-1", justification="need")

        call_kwargs = mock_britive_client.my_access.request_approval.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyAccessCheckoutStatus:
    """Test my_access_checkout_status tool."""

    def test_status_pending(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "PENDING"}

        result = my_access_checkout_status(request_id="req-9", profile_id="prof-1", environment_id="env-1")

        assert result["status"] == "pending"
        mock_britive_client.my_access.checkout.assert_not_called()
        mock_britive_client.my_requests.approval_request_status.assert_called_once_with(
            request_id="req-9", headers=None
        )

    def test_status_approved_returns_creds_when_checked_out(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "APPROVED"}
        # Already provisioned -> credentials are fetched and attached.
        mock_britive_client.my_access.checkout.return_value = {"transactionId": "tx-9", "status": "checkedOut"}
        mock_britive_client.my_access.credentials.return_value = {"accessKeyId": "AKIA-test"}

        result = my_access_checkout_status(
            request_id="req-9", profile_id="prof-1", environment_id="env-1", include_credentials=True
        )

        assert result["status"] == "approved"
        assert result["transaction"]["credentials"] == {"accessKeyId": "AKIA-test"}
        # The finalize step never blocks on credentials: checkout is called with include_credentials=False.
        mock_britive_client.my_access.checkout.assert_called_once_with(
            profile_id="prof-1",
            environment_id="env-1",
            headers=None,
            include_credentials=False,
            programmatic=False,
            progress_func=None,
        )
        mock_britive_client.my_access.credentials.assert_called_once_with(transaction_id="tx-9", headers=None)

    def test_status_approved_provisioning_when_not_ready(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "APPROVED"}
        # Still provisioning -> do NOT block fetching credentials; report provisioning instead.
        mock_britive_client.my_access.checkout.return_value = {"transactionId": "tx-9", "status": "checkOutSubmitted"}

        result = my_access_checkout_status(
            request_id="req-9", profile_id="prof-1", environment_id="env-1", include_credentials=True
        )

        assert result["status"] == "provisioning"
        assert result["transaction_id"] == "tx-9"
        mock_britive_client.my_access.credentials.assert_not_called()

    def test_status_rejected(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "REJECTED"}

        result = my_access_checkout_status(request_id="req-9", profile_id="prof-1", environment_id="env-1")

        assert result["status"] == "rejected"
        mock_britive_client.my_access.checkout.assert_not_called()

    def test_status_obo_passes_header(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "PENDING"}

        my_access_checkout_status(request_id="req-9", profile_id="prof-1", environment_id="env-1")

        call_kwargs = mock_britive_client.my_requests.approval_request_status.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyAccessCheckin:
    """Test my_access_checkin tool."""

    def test_checkin(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkin

        mock_britive_client.my_access.checkin.return_value = {"status": "checked_in"}

        result = my_access_checkin(transaction_id="tx-123")

        mock_britive_client.my_access.checkin.assert_called_once_with(
            transaction_id="tx-123",
            headers=None,
        )
        assert result == {"status": "checked_in"}

    def test_checkin_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_checkin

        my_access_checkin(transaction_id="tx-123")

        call_kwargs = mock_britive_client.my_access.checkin.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyAccessListProfiles:
    """Test my_access_list_profiles tool."""

    def test_list_profiles(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_list_profiles

        expected = [{"profileId": "p1", "name": "Admin"}]
        mock_britive_client.my_access.list_profiles.return_value = expected

        result = my_access_list_profiles()

        mock_britive_client.my_access.list_profiles.assert_called_once_with(headers=None)
        assert result == expected

    def test_list_profiles_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_list_profiles

        my_access_list_profiles()

        call_kwargs = mock_britive_client.my_access.list_profiles.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyAccessWhoami:
    """Test my_access_whoami tool."""

    def test_whoami(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_whoami

        expected = {"username": "testuser", "type": "User"}
        mock_britive_client.my_access.whoami.return_value = expected

        result = my_access_whoami()

        mock_britive_client.my_access.whoami.assert_called_once_with(headers=None)
        assert result == expected

    def test_whoami_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_access import my_access_whoami

        my_access_whoami()

        call_kwargs = mock_britive_client.my_access.whoami.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}
