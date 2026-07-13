"""Tests for MCP runner and conditional tool loading."""

from unittest.mock import MagicMock, patch

import pytest


class TestMcpRunner:
    """Test the run() function and OBO-based tool loading."""

    @patch("britive_mcp_tools.core.mcp_runner.importlib.import_module")
    @patch("britive_mcp_tools.core.mcp_runner.mcp")
    def test_non_obo_loads_all_modules(self, mock_mcp, mock_import):
        mock_mcp.client.obo = False

        from britive_mcp_tools.core.mcp_runner import _NON_OBO_MODULES, run

        run()

        # Should import all non-OBO modules
        assert mock_import.call_count == len(_NON_OBO_MODULES)
        for module_name in _NON_OBO_MODULES:
            mock_import.assert_any_call(module_name)
        mock_mcp.run.assert_called_once()

    @patch("britive_mcp_tools.core.mcp_runner.importlib.import_module")
    @patch("britive_mcp_tools.core.mcp_runner.mcp")
    def test_obo_skips_non_obo_modules(self, mock_mcp, mock_import):
        mock_mcp.client.obo = True

        from britive_mcp_tools.core.mcp_runner import run

        run()

        # Should NOT import any non-OBO modules
        mock_import.assert_not_called()
        mock_mcp.run.assert_called_once()

    def test_non_obo_modules_list_is_complete(self):
        from britive_mcp_tools.core.mcp_runner import _NON_OBO_MODULES

        expected_modules = [
            "britive_mcp_tools.tools.application_management_applications",
            "britive_mcp_tools.tools.audit_logs_logs",
            "britive_mcp_tools.tools.identity_management_service_identities",
            "britive_mcp_tools.tools.identity_management_tags",
            "britive_mcp_tools.tools.identity_management_users",
            "britive_mcp_tools.tools.notification_mediums",
            "britive_mcp_tools.tools.reports",
            "britive_mcp_tools.tools.security_active_sessions",
        ]
        assert _NON_OBO_MODULES == expected_modules


class TestBritiveMCPInit:
    """Test BritiveMCP class initialization."""

    def test_mcp_has_client(self):
        from britive_mcp_tools.core.mcp_init import mcp

        assert hasattr(mcp, "client")
        assert mcp.client is not None

    def test_mcp_has_name(self):
        from britive_mcp_tools.core.mcp_init import mcp

        assert mcp.name == "Britive Tool Server"
