"""
Unit tests for the PermissionEngine.

Uses mocked repositories to isolate engine logic from the database.

Tests verify:
- Admin scopes ('admin:all', 'document:admin') bypass ACL checks
- Inactive or missing users receive no scopes
- Access is denied when no ACL matches exist
- Access is granted when an ACL match meets required level
- Exact level match is sufficient for access
- Lower-level grants are insufficient for higher-level requirements
- Invalid required_level raises ValueError
- Multiple ACL entries use the highest granted level
"""
import uuid
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

from app.permissions.engine import PermissionEngine, PERMISSION_LEVELS
from app.core.exceptions import PermissionDeniedError


def make_permission(level: str, user_id: uuid.UUID | None = None, group_id: uuid.UUID | None = None):
    """Helper factory for mock Permission objects."""
    perm = MagicMock()
    perm.level = level
    perm.user_id = user_id
    perm.group_id = group_id
    return perm


def make_user(is_active: bool = True, roles=None):
    """Helper factory for mock User objects."""
    user = MagicMock()
    user.is_active = is_active
    user.roles = roles or []
    return user


@pytest.fixture
def user_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def document_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def mock_perm_repo():
    return AsyncMock()


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def engine(mock_perm_repo) -> PermissionEngine:
    return PermissionEngine(mock_perm_repo)


class TestPermissionEngineLevelMap:

    def test_permission_level_hierarchy(self):
        """read < write < admin by integer values."""
        assert PERMISSION_LEVELS["read"] < PERMISSION_LEVELS["write"]
        assert PERMISSION_LEVELS["write"] < PERMISSION_LEVELS["admin"]

    def test_invalid_level_raises_value_error(self, engine, mock_db, user_id, document_id):
        """Passing an unrecognised required_level must raise ValueError synchronously."""
        with pytest.raises(ValueError, match="Invalid required permission level"):
            import asyncio
            asyncio.run(
                engine.has_document_access(user_id, document_id, "superadmin", mock_db)
            )


@pytest.mark.asyncio
class TestPermissionEngineAccess:

    async def test_admin_all_scope_bypasses_acl(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """User with 'admin:all' scope must bypass ACL check and return True."""
        role = MagicMock()
        role.scopes = ["admin:all"]
        user = make_user(roles=[role])

        # Mock DB query to return our user
        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        result = await engine.has_document_access(user_id, document_id, "admin", mock_db)
        assert result is True
        # ACL repo should NOT have been called at all
        mock_perm_repo.get_matching_permissions.assert_not_called()

    async def test_document_admin_scope_bypasses_acl(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """User with 'document:admin' scope must bypass ACL check."""
        role = MagicMock()
        role.scopes = ["document:admin"]
        user = make_user(roles=[role])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        result = await engine.has_document_access(user_id, document_id, "read", mock_db)
        assert result is True

    async def test_no_acl_match_raises_permission_denied(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """When no ACL entries match, PermissionDeniedError must be raised."""
        user = make_user(roles=[])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        mock_perm_repo.get_user_group_ids.return_value = []
        mock_perm_repo.get_matching_permissions.return_value = []

        with pytest.raises(PermissionDeniedError):
            await engine.has_document_access(user_id, document_id, "read", mock_db)

    async def test_exact_level_match_grants_access(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """When granted level exactly matches required level, access is granted."""
        user = make_user(roles=[])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        mock_perm_repo.get_user_group_ids.return_value = []
        mock_perm_repo.get_matching_permissions.return_value = [
            make_permission("write", user_id=user_id)
        ]

        result = await engine.has_document_access(user_id, document_id, "write", mock_db)
        assert result is True

    async def test_higher_grant_satisfies_lower_requirement(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """An 'admin' grant must satisfy a 'read' requirement."""
        user = make_user(roles=[])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        mock_perm_repo.get_user_group_ids.return_value = []
        mock_perm_repo.get_matching_permissions.return_value = [
            make_permission("admin", user_id=user_id)
        ]

        result = await engine.has_document_access(user_id, document_id, "read", mock_db)
        assert result is True

    async def test_lower_grant_insufficient_for_higher_requirement(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """A 'read' grant must NOT satisfy an 'admin' requirement."""
        user = make_user(roles=[])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        mock_perm_repo.get_user_group_ids.return_value = []
        mock_perm_repo.get_matching_permissions.return_value = [
            make_permission("read", user_id=user_id)
        ]

        with pytest.raises(PermissionDeniedError):
            await engine.has_document_access(user_id, document_id, "admin", mock_db)

    async def test_group_permission_grants_access(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """ACL grant via group membership must be honoured."""
        group_id = uuid.uuid4()
        user = make_user(roles=[])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        mock_perm_repo.get_user_group_ids.return_value = [group_id]
        mock_perm_repo.get_matching_permissions.return_value = [
            make_permission("write", group_id=group_id)
        ]

        result = await engine.has_document_access(user_id, document_id, "read", mock_db)
        assert result is True

    async def test_highest_level_used_from_multiple_grants(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """When multiple ACL entries exist, the highest level is used for evaluation."""
        group_id = uuid.uuid4()
        user = make_user(roles=[])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        mock_perm_repo.get_user_group_ids.return_value = [group_id]
        mock_perm_repo.get_matching_permissions.return_value = [
            make_permission("read", user_id=user_id),
            make_permission("admin", group_id=group_id),
        ]

        # 'admin' grant in the list should satisfy an 'admin' requirement
        result = await engine.has_document_access(user_id, document_id, "admin", mock_db)
        assert result is True

    async def test_inactive_user_gets_no_scopes(self, engine, mock_perm_repo, mock_db, user_id, document_id):
        """Inactive users return an empty scopes list so no RBAC bypass occurs."""
        user = make_user(is_active=False, roles=[MagicMock(scopes=["admin:all"])])

        result_mock = MagicMock()
        result_mock.scalars.return_value.first.return_value = user
        mock_db.execute.return_value = result_mock

        mock_perm_repo.get_user_group_ids.return_value = []
        mock_perm_repo.get_matching_permissions.return_value = []

        # Inactive user should not bypass via RBAC, so ACL check fails
        with pytest.raises(PermissionDeniedError):
            await engine.has_document_access(user_id, document_id, "read", mock_db)
