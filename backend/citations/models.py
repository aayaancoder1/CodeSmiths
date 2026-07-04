from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class SourceReference:
    """
    Tracks reference parameters linking directly to an extraction source.
    """
    source_id: str
    type: str  # e.g. "chunk", "graph_node", "graph_edge"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Citation:
    """
    Maps generated response text segment indices to source attributes.
    """
    citation_id: str
    text_span: List[int]  # [start_char_idx, end_char_idx]
    sources: List[SourceReference] = field(default_factory=list)
    confidence_score: float = 1.0

@dataclass
class ProvenanceMap:
    """
    Structure tracking how graph entities link back to raw text document fragments.
    """
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    edges: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class CitationPayload:
    """
    Complete return model containing parsed citations and lineage mappings.
    """
    citations: List[Citation]
    provenance: ProvenanceMap
