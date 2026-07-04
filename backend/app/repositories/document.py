from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Chunk, Document, DocumentVersion
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """DocumentRepository subclassing BaseRepository for the Document model."""

    def __init__(self, db: AsyncSession):
        super().__init__(Document, db)

    async def get_with_versions(self, document_id: UUID) -> Document | None:
        """Fetch a document along with all its version records."""
        query = (
            select(Document)
            .filter(Document.id == document_id)
            .options(selectinload(Document.versions))
        )
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_active_version(self, document_id: UUID) -> DocumentVersion | None:
        """Fetch the active version of a document."""
        query = (
            select(DocumentVersion)
            .filter(
                DocumentVersion.document_id == document_id,
                DocumentVersion.is_active == True
            )
        )
        # Apply tenant filter manually since we are querying DocumentVersion directly
        if hasattr(DocumentVersion, "tenant_id"):
            query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_version(self, version_obj: DocumentVersion) -> DocumentVersion:
        """Insert a new document version, scoped by tenant."""
        if hasattr(version_obj, "tenant_id"):
            from app.core.context import get_current_tenant_id
            from app.core.exceptions import TenantIsolationError
            tenant_id = get_current_tenant_id()
            if not tenant_id:
                raise TenantIsolationError("Tenant context missing for version creation.")
            version_obj.tenant_id = tenant_id

        self.db.add(version_obj)
        await self.db.flush()
        return version_obj

    async def create_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        """Bulk insert text chunks for a document version."""
        from app.core.context import get_current_tenant_id
        from app.core.exceptions import TenantIsolationError
        tenant_id = get_current_tenant_id()
        if not tenant_id:
            raise TenantIsolationError("Tenant context missing for chunk bulk insertion.")

        for chunk in chunks:
            chunk.tenant_id = tenant_id
            self.db.add(chunk)

        await self.db.flush()
        return chunks

    async def get_chunks_for_version(self, version_id: UUID) -> List[Chunk]:
        """Fetch all text chunks associated with a specific document version."""
        query = select(Chunk).filter(Chunk.version_id == version_id).order_by(Chunk.chunk_number.asc())
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return list(result.scalars().all())
