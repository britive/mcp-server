"""Tests for BritiveClientWrapper authentication logic."""

import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from britive_mcp_tools.auth.client_wrapper import BritiveClientWrapper


class TestBritiveClientWrapperInit:
    """Test BritiveClientWrapper initialization."""

    def test_init_with_static_token(self, monkeypatch):
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "my-token")
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        wrapper = BritiveClientWrapper("test-tenant")

        assert wrapper.tenant == "test-tenant"
        assert wrapper.tenant_dns == "test-tenant"
        assert wrapper.obo is False
        assert wrapper.email is None

    def test_init_with_obo(self, monkeypatch):
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "my-token")
        monkeypatch.setenv("BRITIVE_EMAIL", "user@example.com")

        wrapper = BritiveClientWrapper("test-tenant")

        assert wrapper.obo is True
        assert wrapper.email == "user@example.com"

    def test_init_without_obo(self, monkeypatch):
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "my-token")
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        wrapper = BritiveClientWrapper("test-tenant")

        assert wrapper.obo is False
        assert wrapper.email is None


class TestGetTenantDns:
    """Test tenant DNS resolution."""

    def test_static_token_returns_tenant_directly(self, monkeypatch):
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "my-token")
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        wrapper = BritiveClientWrapper("my-company")
        assert wrapper.tenant_dns == "my-company"

    @patch("britive_mcp_tools.auth.client_wrapper.ConfigParser")
    def test_cli_auth_reads_config(self, mock_config_cls, monkeypatch):
        monkeypatch.delenv("BRITIVE_STATIC_TOKEN", raising=False)
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        mock_config = MagicMock()
        mock_config.__getitem__ = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value="my-company.britive.com"))
        )
        mock_config_cls.return_value = mock_config

        wrapper = BritiveClientWrapper("my-company")

        mock_config.read.assert_called_once()
        assert wrapper.tenant_dns == "my-company.britive.com"

    @patch("britive_mcp_tools.auth.client_wrapper.ConfigParser")
    def test_cli_auth_missing_tenant_raises(self, mock_config_cls, monkeypatch):
        monkeypatch.delenv("BRITIVE_STATIC_TOKEN", raising=False)
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        mock_config = MagicMock()
        mock_config.__getitem__ = MagicMock(side_effect=KeyError("tenant-missing"))
        mock_config_cls.return_value = mock_config

        with pytest.raises(KeyError, match="User not authenticated"):
            BritiveClientWrapper("missing")


class TestGetToken:
    """Test token retrieval."""

    def test_static_token(self, monkeypatch):
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "static-token-value")
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        wrapper = BritiveClientWrapper("test-tenant")
        assert wrapper.get_token() == "static-token-value"

    @patch("britive_mcp_tools.auth.client_wrapper.britive_cli.BritiveCli")
    @patch("britive_mcp_tools.auth.client_wrapper.ConfigParser")
    def test_cli_token(self, mock_config_cls, mock_cli_cls, monkeypatch):
        monkeypatch.delenv("BRITIVE_STATIC_TOKEN", raising=False)
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        # Setup config mock
        mock_config = MagicMock()
        mock_config.__getitem__ = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value="tenant.britive.com"))
        )
        mock_config_cls.return_value = mock_config

        # Setup CLI mock
        mock_cli = MagicMock()
        mock_cli.credential_manager.credentials = {"accessToken": "cli-token-value"}
        mock_cli_cls.return_value = mock_cli

        wrapper = BritiveClientWrapper("test-tenant")
        token = wrapper.get_token()

        mock_cli.login.assert_called_once()
        mock_cli.set_credential_manager.assert_called_once()
        assert token == "cli-token-value"


class TestGetClient:
    """Test Britive client creation."""

    @patch("britive_mcp_tools.auth.client_wrapper.Britive")
    def test_get_client_creates_britive_instance(self, mock_britive_cls, monkeypatch):
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "my-token")
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        mock_session = MagicMock()
        mock_session.headers = MagicMock()
        mock_session.headers.get.return_value = "Britive SDK/1.0"
        mock_instance = MagicMock()
        mock_instance.session = mock_session
        mock_britive_cls.return_value = mock_instance

        wrapper = BritiveClientWrapper("test-tenant")
        client = wrapper.get_client()

        mock_britive_cls.assert_called_once_with(tenant="test-tenant", token="my-token")
        mock_session.headers.update.assert_called_once()
        # Verify User-Agent includes "Britive MCP Server"
        call_args = mock_session.headers.update.call_args[0][0]
        assert "Britive MCP Server" in call_args["User-Agent"]
        assert client is mock_instance
