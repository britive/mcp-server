"""Tests for notification_mediums tools."""

import pytest


class TestNotificationMediumsList:
    def test_list_no_filter(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_list

        expected = [{"id": "nm1", "name": "slack-alerts", "type": "slack"}]
        mock_britive_client.global_settings.notification_mediums.list.return_value = expected

        result = notification_mediums_list()

        mock_britive_client.global_settings.notification_mediums.list.assert_called_once_with(None)
        assert result == expected

    def test_list_with_filter(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_list

        notification_mediums_list(filter_expression="name co britive")

        mock_britive_client.global_settings.notification_mediums.list.assert_called_once_with("name co britive")


class TestNotificationMediumsCreate:
    def test_create_slack(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_create

        expected = {"id": "nm2", "name": "my-slack", "type": "slack"}
        mock_britive_client.global_settings.notification_mediums.create.return_value = expected

        result = notification_mediums_create(
            notification_medium_type="slack",
            name="my-slack",
            url="https://hooks.slack.com/xxx",
            token="xoxb-token",
            description="Slack alerts",
        )

        mock_britive_client.global_settings.notification_mediums.create.assert_called_once_with(
            notification_medium_type="slack",
            name="my-slack",
            url="https://hooks.slack.com/xxx",
            token="xoxb-token",
            description="Slack alerts",
        )
        assert result == expected

    def test_create_teams_no_token(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_create

        notification_mediums_create(
            notification_medium_type="teams",
            name="my-teams",
            url="https://teams.webhook.com/xxx",
        )

        call_kwargs = mock_britive_client.global_settings.notification_mediums.create.call_args[1]
        assert call_kwargs["token"] is None

    def test_create_webhook(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_create

        notification_mediums_create(
            notification_medium_type="webhook",
            name="my-webhook",
            url="https://example.com/hook",
        )

        mock_britive_client.global_settings.notification_mediums.create.assert_called_once()


class TestNotificationMediumsGet:
    def test_get(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_get

        expected = {"id": "nm1", "name": "slack-alerts", "type": "slack"}
        mock_britive_client.global_settings.notification_mediums.get.return_value = expected

        result = notification_mediums_get(notification_medium_id="nm1")

        mock_britive_client.global_settings.notification_mediums.get.assert_called_once_with("nm1")
        assert result == expected


class TestNotificationMediumsUpdate:
    def test_update(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_update

        params = {"name": "updated-name"}
        notification_mediums_update(notification_medium_id="nm1", parameters=params)

        mock_britive_client.global_settings.notification_mediums.update.assert_called_once_with("nm1", params)


class TestNotificationMediumsDelete:
    def test_delete(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_delete

        notification_mediums_delete(notification_medium_id="nm1")

        mock_britive_client.global_settings.notification_mediums.delete.assert_called_once_with("nm1")


class TestNotificationMediumsGetChannels:
    def test_get_channels(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.notification_mediums import notification_mediums_get_channels

        expected = [{"id": "C01", "name": "#alerts"}]
        mock_britive_client.global_settings.notification_mediums.get_channels.return_value = expected

        result = notification_mediums_get_channels(notification_medium_id="nm1")

        mock_britive_client.global_settings.notification_mediums.get_channels.assert_called_once_with("nm1")
        assert result == expected
