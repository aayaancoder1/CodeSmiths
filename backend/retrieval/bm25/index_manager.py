from abc import ABC, abstractmethod
from typing import List, Dict, Set, Any
from .models import BM25Document

class IIndexManager(ABC):
    """
    Interface for handling inverted index updates, builds, and deletes.
    """

    @abstractmethod
    def add_documents(self, documents: List[BM25Document]) -> None:
        """Add new documents to the inverted index."""
        pass

    @abstractmethod
    def remove_document(self, document_id: str, tenant_id: str) -> None:
        """Remove a document from the index."""
        pass

    @abstractmethod
    def get_document_frequency(self, token: str, tenant_id: str) -> int:
        """Get document frequency (DF) score for a specific term."""
        pass


class MockIndexManager(IIndexManager):
    """
    Placeholder memory index manager.
    """
    def __init__(self):
        self._index: Dict[str, Dict[str, Set[str]]] = {}  # tenant -> term -> document_ids

    def add_documents(self, documents: List[BM25Document]) -> None:
        pass

    def remove_document(self, document_id: str, tenant_id: str) -> None:
        pass

    def get_document_frequency(self, token: str, tenant_id: str) -> int:
        return 1
