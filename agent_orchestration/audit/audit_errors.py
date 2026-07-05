class AuditError(Exception):
    """Base exception for all Audit Agent errors."""
    pass

class AuditStorageError(AuditError):
    """Raised when there's an issue saving or listing from the storage system."""
    pass

class InvalidAuditRecordError(AuditError):
    """Raised when the record structure is invalid or has illegal fields."""
    pass

class MissingAuditFieldError(AuditError):
    """Raised when a required field is missing from the audit record."""
    pass

class DuplicateAuditRecordError(AuditError):
    """Raised when an attempt is made to overwrite an existing record."""
    pass
