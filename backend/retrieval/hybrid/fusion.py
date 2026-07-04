from abc import ABC, abstractmethod
from typing import List, Any
from .models import FusedResult

class IFusionStrategy(ABC):
    """
    Interface for fusing multiple search result lists.
    """

    @abstractmethod
    def fuse(self, vector_results: List[Any], bm25_results: List[Any]) -> List[FusedResult]:
        """Fuses vector and keyword inputs into a single list of results."""
        pass


class ReciprocalRankFusion(IFusionStrategy):
    """
    RRF implementation placeholder.
    """
    def __init__(self, constant: float = 60.0):
        self.constant = constant

    def fuse(self, vector_results: List[Any], bm25_results: List[Any]) -> List[FusedResult]:
        # Placeholder RRF logic
        return [
            FusedResult(
                chunk_id="fused_rrf_1",
                document_id="doc_1",
                text="RRF fusion placeholder content",
                fusion_score=0.032,
                metadata={}
            )
        ]


class WeightedFusion(IFusionStrategy):
    """
    Weighted combination fusion placeholder.
    """
    def __init__(self, vector_weight: float = 0.7, bm25_weight: float = 0.3):
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight

    def fuse(self, vector_results: List[Any], bm25_results: List[Any]) -> List[FusedResult]:
        # Placeholder weighted scores merging
        return [
            FusedResult(
                chunk_id="fused_weighted_1",
                document_id="doc_1",
                text="Weighted fusion placeholder content",
                fusion_score=0.85,
                metadata={}
            )
        ]
