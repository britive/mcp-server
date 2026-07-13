"""Tests for security_active_sessions tools."""

import pytest


class TestSecurityActiveSessionsListUsers:
    def test_list_users_no_search(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.security_active_sessions import (
            security_active_sessions_list_users,
        )

        expected = [{"userId": "u1", "name": "Alice", "countOfProfiles": 2}]
        mock_britive_client.security.active_sessions.list_users.return_value = expected

        result = security_active_sessions_list_users()

        mock_britive_client.security.active_sessions.list_users.assert_called_once_with(None)
        assert result == expected

    def test_list_users_with_search(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.security_active_sessions import (
            security_active_sessions_list_users,
        )

        security_active_sessions_list_users(search_text="alice")

        mock_britive_client.security.active_sessions.list_users.assert_called_once_with("alice")


class TestSecurityActiveSessionsListUserSessions:
    def test_list_user_sessions(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.security_active_sessions import (
            security_active_sessions_list_user_sessions,
        )

        expected = {"applications": [{"papId": "p1", "profileName": "Admin"}]}
        mock_britive_client.security.active_sessions.list_user_sessions.return_value = expected

        result = security_active_sessions_list_user_sessions(user_id="u1")

        mock_britive_client.security.active_sessions.list_user_sessions.assert_called_once_with(
            "u1"
        )
        assert result == expected


class TestSecurityActiveSessionsCheckin:
    def test_checkin(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.security_active_sessions import (
            security_active_sessions_checkin,
        )

        security_active_sessions_checkin(user_id="u1", profile_ids=["p1", "p2"])

        mock_britive_client.security.active_sessions.checkin.assert_called_once_with(
            "u1", ["p1", "p2"]
        )


class TestSecurityActiveSessionsCheckinAll:
    def test_checkin_all(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.security_active_sessions import (
            security_active_sessions_checkin_all,
        )

        security_active_sessions_checkin_all(user_id="u1")

        mock_britive_client.security.active_sessions.checkin_all.assert_called_once_with("u1")
