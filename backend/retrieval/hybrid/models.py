from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class FusedResult:
    """
    Candidate result after applying rank merging, scoring, or fusion.
    """
    chunk_id: str
    document_id: str
    text: str
    fusion_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class HybridSearchInput:
    """
    Input structure containing outcomes from BM25 and Vector search pipelines.
    """
    vector_results: List[Any]
    bm25_results: List[Any]
    tenant_id: str
    query: str
    top_k: int = 10

@dataclass
class HybridSearchOutput:
    """
    Fused and sorted outputs ready to pass to rerank stages.
    """
    merged_results: List[FusedResult]
    source_metadata: Dict[str, Any] = field(default_factory=dict)
