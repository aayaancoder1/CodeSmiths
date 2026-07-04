from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class BM25Filter:
    """
    Metadata filter rules for filtering lexical searches.
    """
    field: str
    operator: str
    value: Any

@dataclass
class BM25Request:
    """
    BM25 query search request payload.
    """
    query: str
    tenant_id: str
    top_k: int = 10
    filters: List[BM25Filter] = field(default_factory=list)

@dataclass
class BM25Document:
    """
    Document schema fed into the index builder.
    """
    document_id: str
    tenant_id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BM25Result:
    """
    Result model returned from lexical search queries.
    """
    chunk_id: str
    document_id: str
    text: str
    score: float
    metadata: Dict[str, Any]
