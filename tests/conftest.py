"""Shared fixtures for Britive MCP Server tests."""

import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    """Set required environment variables before any module-level code runs."""
    monkeypatch.setenv("BRITIVE_TENANT", "test-tenant")
    monkeypatch.setenv("BRITIVE_STATIC_TOKEN", "test-token-123")


@pytest.fixture
def mock_britive_client():
    """Return a fully mocked Britive SDK client."""
    client = MagicMock()
    client.my_access = MagicMock()
    client.my_resources = MagicMock()
    client.my_secrets = MagicMock()
    client.application_management.applications = MagicMock()
    client.audit_logs.logs = MagicMock()
    client.identity_management.users = MagicMock()
    client.identity_management.service_identities = MagicMock()
    client.identity_management.tags = MagicMock()
    client.notification_mediums = MagicMock()
    client.reports = MagicMock()
    client.security.active_sessions = MagicMock()
    return client


@pytest.fixture
def mock_client_wrapper(mock_britive_client):
    """Patch the real client_wrapper object's get_client to return mock.

    Since tool modules hold a direct reference to the client_wrapper object
    (imported at module level), we must patch the object itself, not the
    module attribute.
    """
    from britive_mcp_tools.core.mcp_init import client_wrapper

    original_obo = client_wrapper.obo
    original_email = client_wrapper.email

    with patch.object(client_wrapper, "get_client", return_value=mock_britive_client):
        client_wrapper.obo = False
        client_wrapper.email = None
        yield client_wrapper

    client_wrapper.obo = original_obo
    client_wrapper.email = original_email


@pytest.fixture
def mock_client_wrapper_obo(mock_britive_client):
    """Patch client_wrapper with OBO mode enabled."""
    from britive_mcp_tools.core.mcp_init import client_wrapper

    original_obo = client_wrapper.obo
    original_email = client_wrapper.email

    with patch.object(client_wrapper, "get_client", return_value=mock_britive_client):
        client_wrapper.obo = True
        client_wrapper.email = "obo-user@example.com"
        yield client_wrapper

    client_wrapper.obo = original_obo
    client_wrapper.email = original_email
