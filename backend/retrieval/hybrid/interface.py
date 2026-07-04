from abc import ABC, abstractmethod
from typing import List, Any
from .models import HybridSearchInput, HybridSearchOutput, FusedResult

class IHybridRetrievalService(ABC):
    """
    Interface for merging BM25 and Vector search results.
    """

    @abstractmethod
    def hybrid_search(self, inputs: HybridSearchInput) -> HybridSearchOutput:
        """Combine BM25 and Vector queries into a single hybrid collection."""
        pass

    @abstractmethod
    def reciprocal_rank_fusion(self, vector_results: List[Any], bm25_results: List[Any], k: int = 60) -> List[FusedResult]:
        """Apply Reciprocal Rank Fusion (RRF) to blend rankings."""
        pass

    @abstractmethod
    def aggregate_results(self, vector_results: List[Any], bm25_results: List[Any]) -> List[FusedResult]:
        """Deduplicate and group multiple search inputs."""
        pass

    @abstractmethod
    def rerank_results(self, results: List[FusedResult], query: str) -> List[FusedResult]:
        """Rerank candidates using semantic scoring models."""
        pass
