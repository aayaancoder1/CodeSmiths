from abc import ABC, abstractmethod
from typing import List

class IBM25Scorer(ABC):
    """
    Interface defining lexical BM25 calculations.
    """

    @abstractmethod
    def calculate_score(
        self, 
        query_tokens: List[str], 
        doc_tokens: List[str], 
        doc_frequency: int, 
        total_docs: int, 
        avg_doc_len: float
    ) -> float:
        """Compute the BM25 term weighting score for a tokenized pair."""
        pass

class BM25Scorer(IBM25Scorer):
    """
    Placeholder configuration scorer for lexical indexing.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b

    def calculate_score(
        self, 
        query_tokens: List[str], 
        doc_tokens: List[str], 
        doc_frequency: int, 
        total_docs: int, 
        avg_doc_len: float
    ) -> float:
        # Placeholder score return
        return 1.0
