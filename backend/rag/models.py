from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class RagRequest:
    """
    RAG input payload representing query strings and tenant isolation boundaries.
    """
    query: str
    tenant_id: str
    filters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExpandedGraphContext:
    """
    Isolated node and edge definitions parsed from Neo4j traversal.
    """
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    edges: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class AssembledContext:
    """
    Unified context block incorporating text chunks and graph data.
    """
    retrieved_chunks: List[Dict[str, Any]] = field(default_factory=list)
    graph_context: ExpandedGraphContext = field(default_factory=lambda: ExpandedGraphContext())

@dataclass
class RagPrompt:
    """
    Formatted prompt parameters generated for LLM APIs.
    """
    system_instruction: str
    user_prompt: str

@dataclass
class RagResponse:
    """
    Response details returned back to requesting applications.
    """
    answer: str
    context: AssembledContext
    metadata: Dict[str, Any] = field(default_factory=dict)
