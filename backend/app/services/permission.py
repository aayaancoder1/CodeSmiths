import logging
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permission import Permission
from app.repositories import PermissionRepository, AuditRepository
from app.permissions.engine import PermissionEngine
from app.audit import AuditService
from app.core.exceptions import PermissionDeniedError, EntityNotFoundError

logger = logging.getLogger(__name__)


class PermissionService:
    """Service layer managing document access control policies."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.perm_repo = PermissionRepository(db)
        self.permission_engine = PermissionEngine(self.perm_repo)
        self.audit_service = AuditService(AuditRepository(db))

    async def verify_access(self, user_id: UUID, document_id: UUID, required_level: str) -> bool:
        """Helper to quickly check if a user is authorized for document actions (returns True or raises Exception)."""
        return await self.permission_engine.has_document_access(
            user_id=user_id, document_id=document_id, required_level=required_level, db=self.db
        )

    async def list_acl_for_document(self, document_id: UUID, user_id: UUID) -> List[Permission]:
        """Fetch all ACL settings for a document. Enforces that the requesting user has administrative rights."""
        # Validate that requesting user has 'admin' rights on the document
        await self.permission_engine.has_document_access(
            user_id=user_id, document_id=document_id, required_level="admin", db=self.db
        )

        return await self.perm_repo.get_acl_for_document(document_id)

    async def grant_permission(
        self,
        document_id: UUID,
        grantor_user_id: UUID,
        principal_id: UUID,
        principal_type: str,
        level: str,
    ) -> Permission:
        """Create a new ACL entry granting a User or Group access. Requires administrative rights."""
        # 1. Enforce that grantor has administrative rights on the document
        await self.permission_engine.has_document_access(
            user_id=grantor_user_id, document_id=document_id, required_level="admin", db=self.db
        )

        # 2. Build permission record params
        perm_data = {
            "document_id": document_id,
            "level": level,
        }
        if principal_type == "user":
            perm_data["user_id"] = principal_id
        elif principal_type == "group":
            perm_data["group_id"] = principal_id
        else:
            raise ValueError("Invalid principal_type. Must be 'user' or 'group'.")

        # 3. Create the rule
        perm = await self.perm_repo.create(perm_data)

        # 4. Compliance Audit
        await self.audit_service.log_action(
            operation="permission.grant",
            status="success",
            user_id=grantor_user_id,
            document_id=document_id,
            details={
                "granted_to": str(principal_id),
                "principal_type": principal_type,
                "level": level
            }
        )

        return perm

    async def revoke_permission(self, permission_id: UUID, grantor_user_id: UUID) -> Permission:
        """Remove an ACL entry. Requires administrative rights on the document."""
        # 1. Fetch permission record
        perm = await self.perm_repo.get(permission_id)
        if not perm:
            raise EntityNotFoundError("Permission", permission_id)

        # 2. Enforce that grantor has admin access on the document associated with the permission
        await self.permission_engine.has_document_access(
            user_id=grantor_user_id, document_id=perm.document_id, required_level="admin", db=self.db
        )

        # 3. Revoke permission
        await self.perm_repo.remove(permission_id)

        # 4. Compliance Audit
        await self.audit_service.log_action(
            operation="permission.revoke",
            status="success",
            user_id=grantor_user_id,
            document_id=perm.document_id,
            details={
                "revoked_from": str(perm.user_id or perm.group_id),
                "principal_type": "user" if perm.user_id else "group"
            }
        )

        return perm
