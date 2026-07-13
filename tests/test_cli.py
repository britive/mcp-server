"""Tests for CLI entry point and argument parsing."""

import os
from unittest.mock import patch

import pytest

from britive_mcp_tools import main


class TestCliArgParsing:
    """Test CLI argument parsing and environment variable handling."""

    @patch("britive_mcp_tools.core.mcp_runner.run")
    def test_tenant_from_env(self, mock_run, monkeypatch):
        monkeypatch.setenv("BRITIVE_TENANT", "env-tenant")
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "token")
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        with patch("sys.argv", ["britive-mcp"]):
            main()

        assert os.environ["BRITIVE_TENANT"] == "env-tenant"

    @patch("britive_mcp_tools.core.mcp_runner.run")
    def test_tenant_from_cli_overrides_env(self, mock_run, monkeypatch):
        monkeypatch.setenv("BRITIVE_TENANT", "env-tenant")
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "token")

        with patch("sys.argv", ["britive-mcp", "--tenant", "cli-tenant"]):
            main()

        assert os.environ["BRITIVE_TENANT"] == "cli-tenant"

    @patch("britive_mcp_tools.core.mcp_runner.run")
    def test_token_set_in_env(self, mock_run, monkeypatch):
        monkeypatch.setenv("BRITIVE_TENANT", "t")
        monkeypatch.delenv("BRITIVE_STATIC_TOKEN", raising=False)
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        with patch("sys.argv", ["britive-mcp", "--tenant", "t", "--token", "cli-token"]):
            main()

        assert os.environ["BRITIVE_STATIC_TOKEN"] == "cli-token"

    @patch("britive_mcp_tools.core.mcp_runner.run")
    def test_email_set_in_env(self, mock_run, monkeypatch):
        monkeypatch.setenv("BRITIVE_TENANT", "t")
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "token")

        with patch("sys.argv", ["britive-mcp", "--tenant", "t", "--email", "user@test.com"]):
            main()

        assert os.environ["BRITIVE_EMAIL"] == "user@test.com"

    def test_missing_tenant_exits(self, monkeypatch):
        monkeypatch.delenv("BRITIVE_TENANT", raising=False)

        with patch("sys.argv", ["britive-mcp"]):
            with pytest.raises(SystemExit):
                main()

    @patch("britive_mcp_tools.core.mcp_runner.run")
    def test_no_token_does_not_set_env(self, mock_run, monkeypatch):
        monkeypatch.setenv("BRITIVE_TENANT", "t")
        monkeypatch.delenv("BRITIVE_STATIC_TOKEN", raising=False)
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        with patch("sys.argv", ["britive-mcp", "--tenant", "t"]):
            main()

        assert "BRITIVE_STATIC_TOKEN" not in os.environ

    @patch("britive_mcp_tools.core.mcp_runner.run")
    def test_no_email_does_not_set_env(self, mock_run, monkeypatch):
        monkeypatch.setenv("BRITIVE_TENANT", "t")
        monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "token")
        monkeypatch.delenv("BRITIVE_EMAIL", raising=False)

        with patch("sys.argv", ["britive-mcp", "--tenant", "t"]):
            main()

        assert "BRITIVE_EMAIL" not in os.environ
