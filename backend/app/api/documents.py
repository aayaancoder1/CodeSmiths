import uuid
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.dependencies.context import get_tenant_id, get_user_id
from app.schemas.document import DocumentResponse, DocumentUploadResponse
from app.services.document import DocumentService
from app.services.ingestion import IngestionService
from app.connectors.base import ConnectorDocument
from app.repositories.permission import PermissionRepository
from app.core.exceptions import BrainException, EntityNotFoundError, PermissionDeniedError

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and ingest a document",
    description="Manually upload a document. It will be parsed, chunked, and stored, and the uploading user will be granted administrator access."
)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(None),
    source: str = Form("upload"),
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    user_id: uuid.UUID = Depends(get_user_id)
):
    """Processes manual file uploads via FastAPI multi-part form data."""
    try:
        content = await file.read()
        filename = file.filename or "uploaded_file"
        file_extension = f".{filename.split('.')[-1]}" if "." in filename else ""

        # Create the standardized ConnectorDocument payload
        conn_doc = ConnectorDocument(
            source_id=filename,
            title=title or filename,
            content=content,
            mime_type=file.content_type or "application/octet-stream",
            file_extension=file_extension,
            metadata={"storage_path": f"uploads/{filename}"}
        )

        ingestion_service = IngestionService(db)
        doc = await ingestion_service.ingest_connector_document(conn_doc, source)

        # Ensure the creator has administrative permission over this uploaded document
        perm_repo = PermissionRepository(db)
        existing_perms = await perm_repo.get_acl_for_document(doc.id)
        if not any(p.user_id == user_id for p in existing_perms):
            await perm_repo.create({
                "document_id": doc.id,
                "user_id": user_id,
                "level": "admin"
            })

        await db.commit()

        # Fetch active version to get correct chunk count
        active_ver = await doc.versions[0] if doc.versions else None
        chunks_count = 0
        if doc.id:
            from app.repositories.document import DocumentRepository
            doc_repo = DocumentRepository(db)
            active_ver = await doc_repo.get_active_version(doc.id)
            if active_ver:
                chunks = await doc_repo.get_chunks_for_version(active_ver.id)
                chunks_count = len(chunks)

        return DocumentUploadResponse(
            document_id=doc.id,
            title=doc.title,
            version=doc.current_version,
            chunks_count=chunks_count
        )

    except BrainException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during upload: {str(e)}"
        )


@router.get(
    "",
    response_model=List[DocumentResponse],
    summary="List all tenant documents",
    description="Retrieve all active documents scoped to the authenticated tenant."
)
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    user_id: uuid.UUID = Depends(get_user_id)
):
    doc_service = DocumentService(db)
    docs = await doc_service.list_documents(skip=skip, limit=limit)
    return docs


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Retrieve document metadata",
    description="Get metadata for a single document. Enforces read ACL permissions."
)
async def get_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    user_id: uuid.UUID = Depends(get_user_id)
):
    doc_service = DocumentService(db)
    try:
        doc = await doc_service.get_document(document_id, user_id=user_id)
        return doc
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)


@router.delete(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Delete a document",
    description="Soft-delete a document container, marking it inactive. Enforces admin/write ACL permissions."
)
async def delete_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    user_id: uuid.UUID = Depends(get_user_id)
):
    doc_service = DocumentService(db)
    try:
        doc = await doc_service.delete_document(document_id, user_id=user_id)
        await db.commit()
        return doc
    except EntityNotFoundError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except PermissionDeniedError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
