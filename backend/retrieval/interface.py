from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import RetrievalRequest, RetrievalResponse, RetrievalFilter

class IRetrievalService(ABC):
    """
    Interface for the Retrieval Service.
    Handles semantic query searches (Vector via Qdrant) and namespace-restricted searches.
    """

    @abstractmethod
    def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        """
        Execute core semantic vector retrieval leveraging the complete payload schema.
        """
        pass

    @abstractmethod
    def similarity_search(self, query_vector: List[float], tenant_id: str, top_k: int = 10) -> RetrievalResponse:
        """
        Queries raw similarity space without additional filters.
        """
        pass

    @abstractmethod
    def filtered_search(self, query_vector: List[float], tenant_id: str, filters: List[RetrievalFilter], top_k: int = 10) -> RetrievalResponse:
        """
        Queries similarity space filtered by specific metadata rules.
        """
        pass

    @abstractmethod
    def namespace_search(self, query_vector: List[float], tenant_id: str, namespace: str, top_k: int = 10) -> RetrievalResponse:
        """
        Queries a specific isolated namespace or directory collection in the vector database.
        """
        pass
