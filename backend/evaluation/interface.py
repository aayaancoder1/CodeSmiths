from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IEvaluationService(ABC):
    """
    Interface for the Evaluation Service.
    Calculates retrieval metrics, citation accuracy, answer quality, and system latencies.
    """

    @abstractmethod
    def evaluate_response(self, query: str, response: Dict[str, Any], ground_truth: Dict[str, Any] = None) -> Dict[str, Any]:
        """Runs benchmarks and compiles metrics on response latency, citation correctness, and answer relevance."""
        pass
