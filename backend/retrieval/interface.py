from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IRetrievalService(ABC):
    """
    Interface for the Retrieval Service.
    Handles semantic query searches (Vector via Qdrant) and lexical searches (BM25),
    applies ACL / permission filtering, and implements hybrid merging logic.
    """

    @abstractmethod
    def retrieve(self, query: str, user_permissions: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Execute hybrid search by:
        1. Querying BM25 indices.
        2. Querying Vector stores.
        3. Applying ACL permission filtering.
        4. Merging and scoring retrieval results.
        """
        pass
