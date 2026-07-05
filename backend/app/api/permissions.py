import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.dependencies.context import get_tenant_id, get_user_id
from app.schemas.permission import (
    PermissionCheckRequest,
    PermissionCheckResponse,
    PermissionGrantRequest,
    PermissionResponse,
)
from app.services.permission import PermissionService
from app.core.exceptions import EntityNotFoundError, PermissionDeniedError

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post(
    "/check",
    response_model=PermissionCheckResponse,
    summary="Check document access",
    description="Evaluate whether the requesting user has the required ACL level for a document."
)
async def check_permission(
    body: PermissionCheckRequest,
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    user_id: uuid.UUID = Depends(get_user_id)
):
    perm_service = PermissionService(db)
    try:
        allowed = await perm_service.verify_access(
            user_id=user_id,
            document_id=body.document_id,
            required_level=body.required_level
        )
        return PermissionCheckResponse(
            allowed=allowed,
            user_id=user_id,
            document_id=body.document_id,
            level=body.required_level
        )
    except PermissionDeniedError:
        return PermissionCheckResponse(
            allowed=False,
            user_id=user_id,
            document_id=body.document_id,
            level=body.required_level
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post(
    "/grant",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Grant document access permission",
    description="Grant read, write, or admin permission on a document to a user or group. Enforces admin rights."
)
async def grant_permission(
    body: PermissionGrantRequest,
    document_id: uuid.UUID = Query(..., description="The document ID to grant permissions for"),
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    user_id: uuid.UUID = Depends(get_user_id)
):
    perm_service = PermissionService(db)
    try:
        perm = await perm_service.grant_permission(
            document_id=document_id,
            grantor_user_id=user_id,
            principal_id=body.principal_id,
            principal_type=body.principal_type,
            level=body.level
        )
        await db.commit()
        return perm
    except PermissionDeniedError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except EntityNotFoundError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/revoke",
    response_model=PermissionResponse,
    summary="Revoke document access permission",
    description="Remove an ACL access policy entry from a document. Enforces admin rights."
)
async def revoke_permission(
    permission_id: uuid.UUID = Query(..., description="The ID of the permission policy to revoke"),
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    user_id: uuid.UUID = Depends(get_user_id)
):
    perm_service = PermissionService(db)
    try:
        perm = await perm_service.revoke_permission(
            permission_id=permission_id,
            grantor_user_id=user_id
        )
        await db.commit()
        return perm
    except PermissionDeniedError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except EntityNotFoundError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
