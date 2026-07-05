from typing import Dict, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth import User, Role
from app.repositories.permission import PermissionRepository
from app.core.exceptions import PermissionDeniedError

# Map permission levels to hierarchy integers for evaluation comparison
PERMISSION_LEVELS: Dict[str, int] = {
    "read": 1,
    "write": 2,
    "admin": 3,
}


class PermissionEngine:
    """Enterprise ACL and RBAC permission evaluation engine."""

    def __init__(self, permission_repo: PermissionRepository):
        self.permission_repo = permission_repo

    async def get_user_roles_and_scopes(self, user_id: UUID, db: AsyncSession) -> List[str]:
        """Fetch all RBAC scopes associated with a user through direct roles."""
        query = select(User).filter(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()
        if not user or not user.is_active:
            return []

        scopes = []
        for role in user.roles:
            scopes.extend(role.scopes)
        return list(set(scopes))

    async def has_document_access(
        self, user_id: UUID, document_id: UUID, required_level: str, db: AsyncSession
    ) -> bool:
        """Validate if a user has access to a document based on system roles and ACL permissions.

        Returns True if authorized, otherwise raises PermissionDeniedError.
        """
        if required_level not in PERMISSION_LEVELS:
            raise ValueError(f"Invalid required permission level: '{required_level}'")

        # 1. RBAC Check (System Administrator Bypass)
        scopes = await self.get_user_roles_and_scopes(user_id, db)
        if "admin:all" in scopes or "document:admin" in scopes:
            # Administrators automatically bypass ACL checks
            return True

        required_int_level = PERMISSION_LEVELS[required_level]

        # 2. Retrieve user groups
        group_ids = await self.permission_repo.get_user_group_ids(user_id)

        # 3. Retrieve matching ACL permissions for this document (direct user or group-based)
        matching_permissions = await self.permission_repo.get_matching_permissions(
            user_id=user_id, group_ids=group_ids, document_id=document_id
        )

        if not matching_permissions:
            # If no explicit ACL matches and user is not admin, deny access
            raise PermissionDeniedError("No matching ACL rule allows access to this document.")

        # 4. Evaluate maximum granted access level in matches
        max_granted_int_level = 0
        for perm in matching_permissions:
            granted_int_level = PERMISSION_LEVELS.get(perm.level, 0)
            if granted_int_level > max_granted_int_level:
                max_granted_int_level = granted_int_level

        # 5. Check if granted level satisfies required level
        if max_granted_int_level >= required_int_level:
            return True

        raise PermissionDeniedError(
            f"Insufficient permission level. Required: '{required_level}', Granted: '{max_granted_int_level}'"
        )
