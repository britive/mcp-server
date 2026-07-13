"""Tests for application_management tools."""

import pytest


class TestApplicationManagementList:
    def test_list_default_extended(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.application_management_applications import (
            application_management_applications_list,
        )

        expected = [{"appId": "a1", "name": "AWS"}]
        mock_britive_client.application_management.applications.list.return_value = expected

        result = application_management_applications_list()

        mock_britive_client.application_management.applications.list.assert_called_once_with(True)
        assert result == expected

    def test_list_not_extended(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.application_management_applications import (
            application_management_applications_list,
        )

        application_management_applications_list(extended=False)

        mock_britive_client.application_management.applications.list.assert_called_once_with(False)


class TestApplicationManagementGet:
    def test_get(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.application_management_applications import (
            application_management_applications_get,
        )

        expected = {"appId": "a1", "name": "AWS", "nativeId": "123456"}
        mock_britive_client.application_management.applications.get.return_value = expected

        result = application_management_applications_get(application_id="a1")

        mock_britive_client.application_management.applications.get.assert_called_once_with("a1")
        assert result == expected
