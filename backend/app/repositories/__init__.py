from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository
from app.repositories.document import DocumentRepository
from app.repositories.permission import PermissionRepository
from app.repositories.audit import AuditRepository
from app.repositories.job import JobRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "DocumentRepository",
    "PermissionRepository",
    "AuditRepository",
    "JobRepository",
]
