from abc import ABC, abstractmethod
from typing import List
from .models import BM25Document, BM25Request, BM25Result

class IBM25RetrievalService(ABC):
    """
    Interface for the BM25 retrieval service.
    Exposes building indices, updating documents, and evaluating matching queries.
    """

    @abstractmethod
    def build_index(self, documents: List[BM25Document]) -> None:
        """Construct the initial BM25 search index."""
        pass

    @abstractmethod
    def update_index(self, documents: List[BM25Document]) -> None:
        """Insert or refresh existing indexed items."""
        pass

    @abstractmethod
    def delete_document(self, document_id: str, tenant_id: str) -> None:
        """Purge document elements from the search index."""
        pass

    @abstractmethod
    def search(self, request: BM25Request) -> List[BM25Result]:
        """Perform lexical keyword searches using terms and filters."""
        pass

    @abstractmethod
    def score(self, query: str, document_id: str, tenant_id: str) -> float:
        """Compute the BM25 match value for a query against a specific document."""
        pass
