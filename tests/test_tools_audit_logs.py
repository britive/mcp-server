"""Tests for audit_logs tools."""

import datetime

import pytest


class TestAuditLogsFields:
    def test_fields(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.audit_logs_logs import audit_logs_logs_fields

        expected = {"actor.displayName": "Actor", "event.displayName": "Event"}
        mock_britive_client.audit_logs.logs.fields.return_value = expected

        result = audit_logs_logs_fields()

        mock_britive_client.audit_logs.logs.fields.assert_called_once()
        assert result == expected


class TestAuditLogsOperators:
    def test_operators(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.audit_logs_logs import audit_logs_logs_operators

        expected = {"eq": "Equals", "co": "Contains"}
        mock_britive_client.audit_logs.logs.operators.return_value = expected

        result = audit_logs_logs_operators()

        mock_britive_client.audit_logs.logs.operators.assert_called_once()
        assert result == expected


class TestAuditLogsQuery:
    def test_query_no_params(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.audit_logs_logs import audit_logs_logs_query

        expected = [{"event": "login", "actor": "bob"}]
        mock_britive_client.audit_logs.logs.query.return_value = expected

        result = audit_logs_logs_query()

        mock_britive_client.audit_logs.logs.query.assert_called_once_with(None, None, None, False)
        assert result == expected

    def test_query_with_all_params(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.audit_logs_logs import audit_logs_logs_query

        from_time = datetime.datetime(2024, 1, 1)
        to_time = datetime.datetime(2024, 1, 31)

        audit_logs_logs_query(
            from_time=from_time,
            to_time=to_time,
            filter_expression='actor.displayName co "bob"',
            csv=True,
        )

        mock_britive_client.audit_logs.logs.query.assert_called_once_with(
            from_time, to_time, 'actor.displayName co "bob"', True
        )
