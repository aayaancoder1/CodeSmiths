import logging
import hashlib
from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.connectors import get_connector_class, ConnectorDocument
from app.parser import get_parser
from app.chunking import RecursiveCharacterChunker
from app.metadata import StandardMetadataExtractor
from app.events import RedisEventPublisher, IndexingEvent
from app.repositories import DocumentRepository, AuditRepository
from app.models.document import Document, DocumentVersion, Chunk
from app.audit import AuditService
from app.core.exceptions import BrainException

logger = logging.getLogger(__name__)


class IngestionService:
    """Service managing the document parsing, chunking, and storage ingestion pipeline."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.doc_repo = DocumentRepository(db)
        self.audit_service = AuditService(AuditRepository(db))
        self.publisher = RedisEventPublisher()
        self.chunker = RecursiveCharacterChunker(chunk_size=1000, chunk_overlap=200)
        self.metadata_extractor = StandardMetadataExtractor()

    async def ingest_connector_document(self, conn_doc: ConnectorDocument, source_type: str) -> Document:
        """Processes a single document payload through the full ingestion pipeline."""
        try:
            # 1. Check if document container already exists
            query_results = await self.db.execute(
                self.doc_repo._apply_tenant_filter(
                    self.doc_repo.model.__table__.select().where(
                        self.doc_repo.model.source == source_type,
                        self.doc_repo.model.original_filename == conn_doc.title  # Heuristic source check
                    )
                )
            )
            existing_doc_row = query_results.first()
            
            # Extract content hash to detect modifications
            content_hash = hashlib.sha256(conn_doc.content).hexdigest()
            
            if existing_doc_row:
                doc_id = existing_doc_row.id
                doc = await self.doc_repo.get(doc_id)
                
                # Retrieve the active version to compare text changes
                active_ver = await self.doc_repo.get_active_version(doc.id)
                
                # 2. Document Parser (Binary -> Plain Text)
                parser = get_parser(mime_type=conn_doc.mime_type, file_extension=conn_doc.file_extension)
                extracted_text = parser.parse(conn_doc.content)
                text_hash = hashlib.sha256(extracted_text.encode("utf-8")).hexdigest()
                
                # Check if content has changed
                if active_ver and hashlib.sha256(active_ver.raw_text.encode("utf-8")).hexdigest() == text_hash:
                    logger.info(f"IngestionService: Document {doc.title} content unchanged. Skipping.")
                    return doc

                # Incremental Update: create new version, mark previous inactive
                if active_ver:
                    active_ver.is_active = False
                    await self.db.flush()

                new_version_num = doc.current_version + 1
                doc.current_version = new_version_num
                doc.title = conn_doc.title
                await self.doc_repo.update(doc, {})
                operation = "update"
            else:
                # 2. Document Parser (Binary -> Plain Text)
                parser = get_parser(mime_type=conn_doc.mime_type, file_extension=conn_doc.file_extension)
                extracted_text = parser.parse(conn_doc.content)
                
                # New Document ingestion
                doc_data = {
                    "title": conn_doc.title,
                    "source": source_type,
                    "original_filename": conn_doc.title,
                    "is_active": True,
                    "current_version": 1
                }
                doc = await self.doc_repo.create(doc_data)
                new_version_num = 1
                operation = "create"

            # 3. Metadata Extraction
            meta = self.metadata_extractor.extract(conn_doc, extracted_text)

            # 4. Save new document version
            ver_obj = DocumentVersion(
                document_id=doc.id,
                version_number=new_version_num,
                word_count=meta.word_count,
                raw_text=extracted_text,
                is_active=True,
                storage_path=conn_doc.metadata.get("storage_path") or ""
            )
            await self.doc_repo.create_version(ver_obj)

            # 5. Text Chunking
            chunks = self.chunker.chunk_text(extracted_text)
            db_chunks = []
            for c in chunks:
                db_chunks.append(
                    Chunk(
                        document_id=doc.id,
                        version_id=ver_obj.id,
                        chunk_number=c.chunk_number,
                        text=c.text,
                        start_offset=c.start_offset,
                        end_offset=c.end_offset,
                        character_count=c.character_count
                    )
                )
            await self.doc_repo.create_chunks(db_chunks)

            # 6. Save standard ACL mappings (if fetched from connector)
            if conn_doc.permissions:
                from app.models.permission import Permission
                from app.repositories.permission import PermissionRepository
                perm_repo = PermissionRepository(self.db)
                for p in conn_doc.permissions:
                    # In a production context, map external email principals to local users/groups
                    # For mockup, we look up direct users or map to default groups
                    is_user = p.principal_type == "user"
                    perm_data = {
                        "document_id": doc.id,
                        "level": p.level,
                    }
                    if is_user:
                        # Find user by email
                        from app.repositories.user import UserRepository
                        user = await UserRepository(self.db).get_by_email(p.principal_id)
                        if user:
                            perm_data["user_id"] = user.id
                            await perm_repo.create(perm_data)
                    else:
                        # Group permission mapping
                        from app.models.auth import Group
                        query = await self.db.execute(
                            perm_repo._apply_tenant_filter(
                                select(Group).filter(Group.name == p.principal_id)
                            )
                        )
                        grp = query.scalars().first()
                        if grp:
                            perm_data["group_id"] = grp.id
                            await perm_repo.create(perm_data)

            # 7. Compliance Audit Log
            await self.audit_service.log_action(
                operation=f"document.{operation}",
                status="success",
                document_id=doc.id,
                details={
                    "version": new_version_num,
                    "chunks_count": len(chunks),
                    "word_count": meta.word_count,
                    "title": doc.title
                }
            )

            # 8. Event Broadcast (to inform downstream vector DBs, Neo4j, etc.)
            event = IndexingEvent(
                event_type=f"document.{operation}d",
                document_id=doc.id,
                source=doc.source,
                tenant_id=doc.tenant_id,
                updated_at=datetime.utcnow(),
                operation=operation,
                version=new_version_num
            )
            await self.publisher.publish(event)

            return doc

        except Exception as e:
            logger.error(f"IngestionService: Ingestion failed for document '{conn_doc.title}': {e}")
            # Audit log ingestion failure
            await self.audit_service.log_action(
                operation="document.ingest_failure",
                status="failure",
                details={
                    "title": conn_doc.title,
                    "source": source_type,
                    "error": str(e)
                }
            )
            raise BrainException(f"Failed to ingest document: {e}", code="INGESTION_PIPELINE_ERROR")

    async def sync_connector(self, connector_type: str, config: dict) -> dict:
        """Instantiate external connector integration and run full sync."""
        conn_cls = get_connector_class(connector_type)
        connector = conn_cls(config)

        stats = {"ingested": 0, "errors": 0}

        try:
            await connector.connect()
            docs = await connector.fetch_documents()

            for doc in docs:
                try:
                    # Ingest document within transaction boundaries
                    await self.ingest_connector_document(doc, connector_type)
                    stats["ingested"] += 1
                except Exception as doc_err:
                    logger.error(f"Failed to ingest synced document {doc.title}: {doc_err}")
                    stats["errors"] += 1
                    # A single document ingestion failure should not stop the synchronization loop
                    continue

            return stats
        finally:
            await connector.disconnect()
