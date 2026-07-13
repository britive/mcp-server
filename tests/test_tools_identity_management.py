"""Tests for identity management tools (users, service identities, tags)."""

import pytest


# --- Users ---

class TestIdentityManagementUsersList:
    def test_list_no_filter(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_users import (
            identity_management_users_list,
        )

        expected = [{"userId": "u1", "username": "alice"}]
        mock_britive_client.identity_management.users.list.return_value = expected

        result = identity_management_users_list()

        mock_britive_client.identity_management.users.list.assert_called_once_with(None, False)
        assert result == expected

    def test_list_with_filter_and_tags(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_users import (
            identity_management_users_list,
        )

        identity_management_users_list(filter_expression='name co "alice"', include_tags=True)

        mock_britive_client.identity_management.users.list.assert_called_once_with(
            'name co "alice"', True
        )


class TestIdentityManagementUsersGet:
    def test_get(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_users import (
            identity_management_users_get,
        )

        expected = {"userId": "u1", "username": "alice", "email": "alice@test.com"}
        mock_britive_client.identity_management.users.get.return_value = expected

        result = identity_management_users_get(user_id="u1")

        mock_britive_client.identity_management.users.get.assert_called_once_with("u1")
        assert result == expected


class TestIdentityManagementUsersSearch:
    def test_search(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_users import (
            identity_management_users_search,
        )

        expected = [{"userId": "u1", "username": "alice"}]
        mock_britive_client.identity_management.users.search.return_value = expected

        result = identity_management_users_search(search_string="alice")

        mock_britive_client.identity_management.users.search.assert_called_once_with("alice")
        assert result == expected


class TestIdentityManagementUsersEnable:
    def test_enable_single(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_users import (
            identity_management_users_enable,
        )

        identity_management_users_enable(user_id="u1")

        mock_britive_client.identity_management.users.enable.assert_called_once_with("u1", None)

    def test_enable_multiple(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_users import (
            identity_management_users_enable,
        )

        identity_management_users_enable(user_ids=["u1", "u2"])

        mock_britive_client.identity_management.users.enable.assert_called_once_with(
            None, ["u1", "u2"]
        )


class TestIdentityManagementUsersDisable:
    def test_disable_single(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_users import (
            identity_management_users_disable,
        )

        identity_management_users_disable(user_id="u1")

        mock_britive_client.identity_management.users.disable.assert_called_once_with("u1", None)


# --- Service Identities ---

class TestIdentityManagementServiceIdentitiesList:
    def test_list(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_service_identities import (
            identity_management_service_identities_list,
        )

        expected = [{"id": "si1", "name": "bot-deploy"}]
        mock_britive_client.identity_management.service_identities.list.return_value = expected

        result = identity_management_service_identities_list()

        mock_britive_client.identity_management.service_identities.list.assert_called_once_with(
            None, False
        )
        assert result == expected


class TestIdentityManagementServiceIdentitiesGet:
    def test_get(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_service_identities import (
            identity_management_service_identities_get,
        )

        expected = {"id": "si1", "name": "bot-deploy", "status": "Active"}
        mock_britive_client.identity_management.service_identities.get.return_value = expected

        result = identity_management_service_identities_get(service_identity_id="si1")

        mock_britive_client.identity_management.service_identities.get.assert_called_once_with(
            "si1"
        )
        assert result == expected


class TestIdentityManagementServiceIdentitiesSearch:
    def test_search(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_service_identities import (
            identity_management_service_identities_search,
        )

        identity_management_service_identities_search(search_string="bot")

        mock_britive_client.identity_management.service_identities.search.assert_called_once_with(
            "bot"
        )


class TestIdentityManagementServiceIdentitiesEnable:
    def test_enable_single(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_service_identities import (
            identity_management_service_identities_enable,
        )

        identity_management_service_identities_enable(service_identity_id="si1")

        mock_britive_client.identity_management.service_identities.enable.assert_called_once_with(
            "si1", None
        )

    def test_enable_multiple(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_service_identities import (
            identity_management_service_identities_enable,
        )

        identity_management_service_identities_enable(service_identity_ids=["si1", "si2"])

        mock_britive_client.identity_management.service_identities.enable.assert_called_once_with(
            None, ["si1", "si2"]
        )


class TestIdentityManagementServiceIdentitiesDisable:
    def test_disable_single(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_service_identities import (
            identity_management_service_identities_disable,
        )

        identity_management_service_identities_disable(service_identity_id="si1")

        mock_britive_client.identity_management.service_identities.disable.assert_called_once_with(
            "si1", None
        )


# --- Tags ---

class TestIdentityManagementTagsList:
    def test_list(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_tags import (
            identity_management_tags_list,
        )

        expected = [{"tagId": "t1", "name": "admins"}]
        mock_britive_client.identity_management.tags.list.return_value = expected

        result = identity_management_tags_list()

        mock_britive_client.identity_management.tags.list.assert_called_once_with(None)
        assert result == expected

    def test_list_with_filter(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_tags import (
            identity_management_tags_list,
        )

        identity_management_tags_list(filter_expression="status eq Active")

        mock_britive_client.identity_management.tags.list.assert_called_once_with(
            "status eq Active"
        )


class TestIdentityManagementTagsGet:
    def test_get(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_tags import (
            identity_management_tags_get,
        )

        expected = {"tagId": "t1", "name": "admins", "status": "Active"}
        mock_britive_client.identity_management.tags.get.return_value = expected

        result = identity_management_tags_get(tag_id="t1")

        mock_britive_client.identity_management.tags.get.assert_called_once_with("t1")
        assert result == expected


class TestIdentityManagementTagsSearch:
    def test_search(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_tags import (
            identity_management_tags_search,
        )

        identity_management_tags_search(search_string="admin")

        mock_britive_client.identity_management.tags.search.assert_called_once_with("admin")


class TestIdentityManagementTagsEnable:
    def test_enable(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_tags import (
            identity_management_tags_enable,
        )

        identity_management_tags_enable(tag_id="t1")

        mock_britive_client.identity_management.tags.enable.assert_called_once_with("t1")


class TestIdentityManagementTagsDisable:
    def test_disable(self, mock_client_wrapper, mock_britive_client):
        from britive_mcp_tools.tools.identity_management_tags import (
            identity_management_tags_disable,
        )

        identity_management_tags_disable(tag_id="t1")

        mock_britive_client.identity_management.tags.disable.assert_called_once_with("t1")
