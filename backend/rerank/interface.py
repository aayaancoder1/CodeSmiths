from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IRerankerService(ABC):
    """
    Interface for the Reranking Service.
    Applies fine-grained semantic reranking (e.g. Cross-Encoders) to optimize top-k results.
    """

    @abstractmethod
    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Rerank candidates based on deep semantic relevance to query."""
        pass
