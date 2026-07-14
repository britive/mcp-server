"""Tests for my_resources tools."""

from unittest.mock import patch

import pytest
from britive.exceptions import (
    ApprovalRequiredButNoJustificationProvided,
    ProfileCheckoutAlreadyApproved,
    StepUpAuthFailed,
    StepUpAuthRequiredButNotProvided,
)
from britive.exceptions.badrequest import PendingProfileApprovalRequestError


class TestMyResourcesList:
    """Test my_resources_list tool."""

    def test_list_no_filter(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_list

        expected = [{"resourceId": "r1", "name": "Linux Server"}]
        mock_britive_client.my_resources.list.return_value = expected

        result = my_resources_list()

        mock_britive_client.my_resources.list.assert_called_once_with(
            list_type=None,
            headers=None,
        )
        assert result == expected

    def test_list_with_type_filter(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_list

        my_resources_list(list_type="databases")

        mock_britive_client.my_resources.list.assert_called_once_with(
            list_type="databases",
            headers=None,
        )

    def test_list_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_list

        my_resources_list()

        call_kwargs = mock_britive_client.my_resources.list.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyResourcesCheckout:
    """Test my_resources_checkout tool (asynchronous, non-blocking)."""

    def test_checkout_no_approval_returns_checked_out(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.return_value = {"transactionId": "tx-456"}

        result = my_resources_checkout(profile_id="prof-1", resource_id="res-1")

        # The probe checkout is attempted with justification withheld so approval-required
        # resources fail fast rather than blocking.
        mock_britive_client.my_resources.checkout.assert_called_once_with(
            profile_id="prof-1",
            resource_id="res-1",
            headers=None,
            include_credentials=False,
            justification=None,
            otp=None,
            progress_func=None,
            response_template=None,
            ticket_id=None,
            ticket_type=None,
        )
        assert result == {"status": "checked_out", "transaction": {"transactionId": "tx-456"}}

    def test_checkout_approval_no_justification_returns_justification_required(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.side_effect = ApprovalRequiredButNoJustificationProvided()

        result = my_resources_checkout(profile_id="prof-1", resource_id="res-1")

        assert result["status"] == "justification_required"
        mock_britive_client.my_resources.request_approval.assert_not_called()

    def test_checkout_approval_with_justification_returns_pending(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.side_effect = ApprovalRequiredButNoJustificationProvided()
        mock_britive_client.my_resources.request_approval.return_value = {"requestId": "req-7"}

        result = my_resources_checkout(
            profile_id="prof-1",
            resource_id="res-1",
            justification="maintenance",
            include_credentials=True,
            response_template="template-1",
            ticket_id="INC-200",
            ticket_type="change",
        )

        assert result["status"] == "pending_approval"
        assert result["request_id"] == "req-7"
        assert result["profile_id"] == "prof-1"
        assert result["resource_id"] == "res-1"
        assert result["include_credentials"] is True
        assert result["response_template"] == "template-1"
        mock_britive_client.my_resources.request_approval.assert_called_once_with(
            justification="maintenance",
            profile_id="prof-1",
            resource_id="res-1",
            block_until_disposition=False,
            ticket_id="INC-200",
            ticket_type="change",
            headers=None,
        )

    def test_checkout_step_up_required_returns_status(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.side_effect = StepUpAuthRequiredButNotProvided()

        result = my_resources_checkout(profile_id="prof-1", resource_id="res-1")

        assert result["status"] == "step_up_otp_required"

    def test_checkout_step_up_failed_returns_status(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.side_effect = StepUpAuthFailed()

        result = my_resources_checkout(profile_id="prof-1", resource_id="res-1", otp="000000")

        assert result["status"] == "step_up_auth_failed"

    def test_checkout_already_pending_returns_pending_approval(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.side_effect = PendingProfileApprovalRequestError()

        result = my_resources_checkout(
            profile_id="prof-1", resource_id="res-1", justification="need it"
        )

        assert result["status"] == "pending_approval"
        assert result["request_id"] is None
        mock_britive_client.my_resources.request_approval.assert_not_called()

    def test_checkout_already_approved_race_returns_checked_out(
        self, mock_client_wrapper, mock_britive_client
    ):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.side_effect = [
            ApprovalRequiredButNoJustificationProvided(),
            {"transactionId": "tx-888"},
        ]
        mock_britive_client.my_resources.request_approval.side_effect = ProfileCheckoutAlreadyApproved()

        result = my_resources_checkout(
            profile_id="prof-1", resource_id="res-1", justification="already ok"
        )

        assert result == {"status": "checked_out", "transaction": {"transactionId": "tx-888"}}

    def test_checkout_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout

        mock_britive_client.my_resources.checkout.return_value = {"transactionId": "tx-456"}

        my_resources_checkout(profile_id="prof-1", resource_id="res-1")

        call_kwargs = mock_britive_client.my_resources.checkout.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyResourcesCheckoutStatus:
    """Test my_resources_checkout_status tool."""

    def test_status_pending(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "PENDING"}

        result = my_resources_checkout_status(request_id="req-7", profile_id="prof-1", resource_id="res-1")

        assert result["status"] == "pending"
        mock_britive_client.my_resources.checkout.assert_not_called()
        mock_britive_client.my_requests.approval_request_status.assert_called_once_with(
            request_id="req-7", headers=None
        )

    def test_status_approved_returns_creds_when_checked_out(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "APPROVED"}
        mock_britive_client.my_resources.checkout.return_value = {"transactionId": "tx-7", "status": "checkedOut"}
        mock_britive_client.my_resources.credentials.return_value = {"accessKeyId": "AKIA-test"}

        result = my_resources_checkout_status(
            request_id="req-7",
            profile_id="prof-1",
            resource_id="res-1",
            include_credentials=True,
            response_template="template-1",
        )

        assert result["status"] == "approved"
        assert result["transaction"]["credentials"] == {"accessKeyId": "AKIA-test"}
        mock_britive_client.my_resources.checkout.assert_called_once_with(
            profile_id="prof-1",
            resource_id="res-1",
            headers=None,
            include_credentials=False,
            otp=None,
            progress_func=None,
            response_template="template-1",
        )
        mock_britive_client.my_resources.credentials.assert_called_once_with(
            transaction_id="tx-7", response_template="template-1", headers=None
        )

    def test_status_approved_provisioning_when_not_ready(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "APPROVED"}
        mock_britive_client.my_resources.checkout.return_value = {"transactionId": "tx-7", "status": "checkOutSubmitted"}

        result = my_resources_checkout_status(
            request_id="req-7", profile_id="prof-1", resource_id="res-1", include_credentials=True
        )

        assert result["status"] == "provisioning"
        assert result["transaction_id"] == "tx-7"
        mock_britive_client.my_resources.credentials.assert_not_called()

    def test_status_approved_step_up_required(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "APPROVED"}
        mock_britive_client.my_resources.checkout.side_effect = StepUpAuthRequiredButNotProvided()

        result = my_resources_checkout_status(request_id="req-7", profile_id="prof-1", resource_id="res-1")

        assert result["status"] == "step_up_otp_required"

    def test_status_approved_forwards_otp(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "APPROVED"}
        mock_britive_client.my_resources.checkout.return_value = {"transactionId": "tx-7", "status": "checkedOut"}

        my_resources_checkout_status(
            request_id="req-7", profile_id="prof-1", resource_id="res-1", otp="123456"
        )

        assert mock_britive_client.my_resources.checkout.call_args[1]["otp"] == "123456"

    def test_status_rejected(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "REJECTED"}

        result = my_resources_checkout_status(request_id="req-7", profile_id="prof-1", resource_id="res-1")

        assert result["status"] == "rejected"
        mock_britive_client.my_resources.checkout.assert_not_called()

    def test_status_obo_passes_header(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkout_status

        mock_britive_client.my_requests.approval_request_status.return_value = {"status": "PENDING"}

        my_resources_checkout_status(request_id="req-7", profile_id="prof-1", resource_id="res-1")

        call_kwargs = mock_britive_client.my_requests.approval_request_status.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyResourcesCheckin:
    """Test my_resources_checkin tool."""

    def test_checkin(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkin

        mock_britive_client.my_resources.checkin.return_value = {"status": "checked_in"}

        result = my_resources_checkin(transaction_id="tx-456")

        mock_britive_client.my_resources.checkin.assert_called_once_with(
            transaction_id="tx-456",
            headers=None,
        )
        assert result == {"status": "checked_in"}

    def test_checkin_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_checkin

        my_resources_checkin(transaction_id="tx-456")

        call_kwargs = mock_britive_client.my_resources.checkin.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMyResourcesListCheckedOutProfiles:
    """Test my_resources_list_checked_out_profiles tool."""

    def test_list_checked_out(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_list_checked_out_profiles

        expected = [{"transactionId": "tx-1", "resourceName": "db-prod"}]
        mock_britive_client.my_resources.list_checked_out_profiles.return_value = expected

        result = my_resources_list_checked_out_profiles()

        mock_britive_client.my_resources.list_checked_out_profiles.assert_called_once_with(
            headers=None,
        )
        assert result == expected

    def test_list_checked_out_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_resources import my_resources_list_checked_out_profiles

        my_resources_list_checked_out_profiles()

        call_kwargs = mock_britive_client.my_resources.list_checked_out_profiles.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}
