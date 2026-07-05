import logging
from typing import Any, Dict
from uuid import UUID
from app.models.audit import AuditLog
from app.repositories.audit import AuditRepository
from app.core.context import get_current_tenant_id, get_current_request_id

logger = logging.getLogger("audit_log")


class AuditService:
    """Service facilitating security and operation audit logs."""

    def __init__(self, audit_repo: AuditRepository):
        self.audit_repo = audit_repo

    async def log_action(
        self,
        operation: str,
        status: str,
        user_id: UUID | None = None,
        document_id: UUID | None = None,
        details: Dict[str, Any] | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        """Record an operation audit log in the database and emit a structured JSON application log."""
        tenant_id = get_current_tenant_id()
        request_id = get_current_request_id()
        details = details or {}

        # 1. Database Persistence
        try:
            db_log = await self.audit_repo.log_event(
                operation=operation,
                status=status,
                user_id=user_id,
                document_id=document_id,
                details=details,
                ip_address=ip_address,
            )
        except Exception as db_err:
            # Prevent database failures from blocking the primary flow
            logger.critical(f"AuditService: Failed to write audit log to database: {db_err}")
            db_log = None

        # 2. Structured JSON Standard Out Logging (for ELK / CloudWatch ingestion)
        structured_log = {
            "event": "audit",
            "request_id": request_id,
            "tenant_id": str(tenant_id) if tenant_id else None,
            "user_id": str(user_id) if user_id else None,
            "document_id": str(document_id) if document_id else None,
            "operation": operation,
            "status": status,
            "ip_address": ip_address,
            "details": details,
        }
        
        # Log via logger matching the result status
        if status == "success":
            logger.info(structured_log)
        else:
            logger.warning(structured_log)

        return db_log
