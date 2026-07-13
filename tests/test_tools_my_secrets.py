"""Tests for my_secrets tools."""

import pytest


class TestMySecretsList:
    """Test my_secrets_list tool."""

    def test_list(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_secrets import my_secrets_list

        expected = [{"path": "/app/db-pass", "name": "db-pass"}]
        mock_britive_client.my_secrets.list.return_value = expected

        result = my_secrets_list()

        mock_britive_client.my_secrets.list.assert_called_once_with(headers=None)
        assert result == expected

    def test_list_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_secrets import my_secrets_list

        my_secrets_list()

        call_kwargs = mock_britive_client.my_secrets.list.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}


class TestMySecretsView:
    """Test my_secrets_view tool."""

    def test_view_basic(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_secrets import my_secrets_view

        expected = {"value": "s3cret"}
        mock_britive_client.my_secrets.view.return_value = expected

        result = my_secrets_view(path="/app/db-pass")

        mock_britive_client.my_secrets.view.assert_called_once_with(
            path="/app/db-pass",
            justification=None,
            otp=None,
            wait_time=60,
            max_wait_time=600,
            headers=None,
        )
        assert result == expected

    def test_view_with_all_params(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.my_secrets import my_secrets_view

        my_secrets_view(
            path="/app/api-key",
            justification="deployment",
            otp="111222",
            wait_time=30,
            max_wait_time=120,
        )

        mock_britive_client.my_secrets.view.assert_called_once_with(
            path="/app/api-key",
            justification="deployment",
            otp="111222",
            wait_time=30,
            max_wait_time=120,
            headers=None,
        )

    def test_view_obo(self, mock_client_wrapper_obo, mock_britive_client):
        from britive_mcp_tools.tools.my_secrets import my_secrets_view

        my_secrets_view(path="/app/db-pass")

        call_kwargs = mock_britive_client.my_secrets.view.call_args[1]
        assert call_kwargs["headers"] == {"X-On-Behalf-Of": "obo-user@example.com"}
