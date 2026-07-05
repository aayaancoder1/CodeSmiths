from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class RetrievalFilter:
    """
    Metadata search filter containing field keys, comparative operator, and value matching criteria.
    """
    field: str
    operator: str  # e.g., "eq", "in", "like"
    value: Any

@dataclass
class RetrievalRequest:
    """
    Payload for a query retrieval request containing target restrictions.
    """
    query: str
    tenant_id: str
    top_k: int = 10
    filters: List[RetrievalFilter] = field(default_factory=list)

@dataclass
class RetrievedChunk:
    """
    A single similarity search item result from the vector database.
    """
    chunk_id: str
    source_id: str
    text: str
    similarity_score: float
    metadata: Dict[str, Any]

@dataclass
class RetrievalResponse:
    """
    Wrapped results returned to the orchestration layer.
    """
    results: List[RetrievedChunk]
