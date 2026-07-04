from dataclasses import dataclass

@dataclass
class RetrievalMetrics:
    """
    Evaluation metrics representing vector and lexical match quality.
    """
    recall_at_k: float
    precision_at_k: float
    mrr: float

@dataclass
class CitationMetrics:
    """
    Attribution verification metrics.
    """
    coverage: float
    correctness: float

@dataclass
class LatencyMetrics:
    """
    Time consumption tracked across different pipeline stages.
    """
    retrieval_ms: float
    graph_ms: float
    total_ms: float

@dataclass
class AnswerMetrics:
    """
    Quality attributes evaluated on final text syntheses.
    """
    faithfulness: float
    relevance: float
    completeness: float

@dataclass
class EvaluationReport:
    """
    Consolidated performance benchmark report.
    """
    query: str
    retrieval: RetrievalMetrics
    citations: CitationMetrics
    latency: LatencyMetrics
    answer: AnswerMetrics
    timestamp: str
