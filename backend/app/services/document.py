import logging
from datetime import datetime
from uuid import UUID
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentVersion
from app.repositories import DocumentRepository, AuditRepository, PermissionRepository
from app.permissions.engine import PermissionEngine
from app.audit import AuditService
from app.events import RedisEventPublisher, IndexingEvent
from app.core.exceptions import PermissionDeniedError, EntityNotFoundError

logger = logging.getLogger(__name__)


class DocumentService:
    """Service layer exposing tenant-scoped document CRUD actions, enforcing ACL validations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.doc_repo = DocumentRepository(db)
        self.permission_engine = PermissionEngine(PermissionRepository(db))
        self.audit_service = AuditService(AuditRepository(db))
        self.publisher = RedisEventPublisher()

    async def get_document(self, doc_id: UUID, user_id: UUID) -> Document:
        """Fetch document details, enforcing ACL read access."""
        # 1. Enforce Permission Check (Raises PermissionDeniedError if unauthorized)
        await self.permission_engine.has_document_access(
            user_id=user_id, document_id=doc_id, required_level="read", db=self.db
        )

        # 2. Retrieve document
        doc = await self.doc_repo.get(doc_id)
        if not doc or not doc.is_active:
            raise EntityNotFoundError("Document", doc_id)

        # 3. Log read action
        await self.audit_service.log_action(
            operation="document.read", status="success", user_id=user_id, document_id=doc_id
        )
        return doc

    async def get_document_raw_text(self, doc_id: UUID, user_id: UUID) -> str:
        """Fetch the raw text content of the active version of a document, enforcing ACL read access."""
        await self.permission_engine.has_document_access(
            user_id=user_id, document_id=doc_id, required_level="read", db=self.db
        )

        active_ver = await self.doc_repo.get_active_version(doc_id)
        if not active_ver:
            raise EntityNotFoundError("DocumentVersion", f"active version for {doc_id}")

        await self.audit_service.log_action(
            operation="document.read_content", status="success", user_id=user_id, document_id=doc_id
        )
        return active_ver.raw_text

    async def list_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """Fetch list of documents scoped to the active tenant."""
        # Note: endpoint checks for tenant scoped access. Global document list filters by tenant.
        query = select(Document).filter(Document.is_active == True).offset(skip).limit(limit)
        query = self.doc_repo._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_document(self, doc_id: UUID, user_id: UUID) -> Document:
        """Soft delete a document, enforcing ACL admin/write validation and broadcasting delete events."""
        # 1. Validate deletion access rights (Requires admin or write level)
        try:
            await self.permission_engine.has_document_access(
                user_id=user_id, document_id=doc_id, required_level="write", db=self.db
            )
        except PermissionDeniedError:
            # Escalating to admin permissions requirement if write fails
            await self.permission_engine.has_document_access(
                user_id=user_id, document_id=doc_id, required_level="admin", db=self.db
            )

        doc = await self.doc_repo.get(doc_id)
        if not doc or not doc.is_active:
            raise EntityNotFoundError("Document", doc_id)

        # 2. Soft delete: flag Document and active versions as inactive
        doc.is_active = False
        await self.doc_repo.update(doc, {})

        active_ver = await self.doc_repo.get_active_version(doc_id)
        if active_ver:
            active_ver.is_active = False
            await self.db.flush()

        # 3. Compliance Audit Log
        await self.audit_service.log_action(
            operation="document.delete",
            status="success",
            user_id=user_id,
            document_id=doc_id,
            details={"title": doc.title}
        )

        # 4. Broadcast Delete Event to downstream systems
        event = IndexingEvent(
            event_type="document.deleted",
            document_id=doc.id,
            source=doc.source,
            tenant_id=doc.tenant_id,
            updated_at=datetime.utcnow(),
            operation="delete",
            version=doc.current_version
        )
        await self.publisher.publish(event)

        return doc
