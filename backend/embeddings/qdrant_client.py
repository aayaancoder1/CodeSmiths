from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IQdrantClient(ABC):
    """
    Interface for the Qdrant database vector store operations.
    """

    @abstractmethod
    def upsert_vectors(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        """Upsert points (IDs, vectors, payloads) to a collection."""
        pass

    @abstractmethod
    def delete_vectors(self, collection_name: str, point_ids: List[str]) -> None:
        """Delete points from a collection by ID."""
        pass

    @abstractmethod
    def delete_by_filter(self, collection_name: str, filter_query: Dict[str, Any]) -> None:
        """Delete points matching a specific metadata filter (e.g. document_id)."""
        pass
