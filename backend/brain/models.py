from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class BrainDocument:
    """
    Unified input payload for document ingestion.
    """
    document_id: str
    tenant_id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BrainQuery:
    """
    Query execution arguments targeting the brain orchestrator.
    """
    query: str
    tenant_id: str
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BrainOutput:
    """
    Consolidated RAG results returned by the integrated pipeline.
    """
    answer: str
    citations: List[Dict[str, Any]] = field(default_factory=list)
    graph_context: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
