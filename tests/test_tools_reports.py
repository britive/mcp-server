"""Tests for reports tools."""

import pytest


class TestReportsList:
    def test_list(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import reports_list

        expected = [{"reportId": "r1", "name": "Profile Historical Access"}]
        mock_britive_client.reports.list.return_value = expected

        result = reports_list()

        mock_britive_client.reports.list.assert_called_once()
        assert result == expected


class TestReportRunProfileHistoricalAccess:
    def test_run_no_filter(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_profile_historical_access

        expected = [{"username": "alice", "profileName": "Admin"}]
        mock_britive_client.reports.run.return_value = expected

        result = report_run_profile_historical_access(report_id="r1")

        mock_britive_client.reports.run.assert_called_once_with("r1", False, None)
        assert result == expected

    def test_run_with_filter_and_csv(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_profile_historical_access

        report_run_profile_historical_access(
            report_id="r1",
            csv=True,
            filter_expression="profileName eq admin",
        )

        mock_britive_client.reports.run.assert_called_once_with(
            "r1", True, "profileName eq admin"
        )


class TestReportRunPermissionsInProfile:
    def test_run(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_permissions_in_profile

        report_run_permissions_in_profile(
            report_id="r2", filter_expression="profile co admin"
        )

        mock_britive_client.reports.run.assert_called_once_with("r2", False, "profile co admin")


class TestReportRunTagMembership:
    def test_run(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_tag_membership

        report_run_tag_membership(report_id="r3")

        mock_britive_client.reports.run.assert_called_once_with("r3", False, None)


class TestReportRunServiceIdentitiesDetails:
    def test_run(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_service_identities_details

        report_run_service_identities_details(
            report_id="r4", filter_expression="name co bot"
        )

        mock_britive_client.reports.run.assert_called_once_with("r4", False, "name co bot")


class TestReportRunUserSecretAccess:
    def test_run(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_user_secret_access

        report_run_user_secret_access(report_id="r5")

        mock_britive_client.reports.run.assert_called_once_with("r5", False, None)


class TestReportRunSecretLastAccess:
    def test_run(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_secret_last_access

        report_run_secret_last_access(report_id="r6", csv=True)

        mock_britive_client.reports.run.assert_called_once_with("r6", True, None)


class TestReportRunPermissionDetails:
    def test_run(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.reports import report_run_permission_details

        report_run_permission_details(
            report_id="r7", filter_expression="application co aws"
        )

        mock_britive_client.reports.run.assert_called_once_with("r7", False, "application co aws")
