from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import RetrievalMetrics, CitationMetrics, LatencyMetrics, AnswerMetrics, EvaluationReport

class IEvaluationService(ABC):
    """
    Interface for scoring system operations and output syntheses.
    """

    @abstractmethod
    def evaluate_retrieval(self, retrieved: List[Any], ground_truth: List[Any]) -> RetrievalMetrics:
        """Score dense and lexical query retrieval relevance."""
        pass

    @abstractmethod
    def evaluate_citations(self, citations: List[Any], ground_truth: List[Any]) -> CitationMetrics:
        """Validate precision, coverage, and correctness of response citations."""
        pass

    @abstractmethod
    def evaluate_latency(self, timings: Dict[str, float]) -> LatencyMetrics:
        """Process processing durations across pipeline layers."""
        pass

    @abstractmethod
    def evaluate_answers(self, answer: str, context: Any, ground_truth: str = None) -> AnswerMetrics:
        """Score answer faithfulness, completeness, and question relevance."""
        pass

    @abstractmethod
    def run_benchmarks(self, dataset: List[Any]) -> List[EvaluationReport]:
        """Perform batch system benchmarks using configured datasets."""
        pass
