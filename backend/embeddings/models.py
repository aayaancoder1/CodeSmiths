from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class EmbeddingMetadata:
    """
    Schema for Embedding Metadata.
    Tracks document details, tenant info, and ACL/permissions.
    """
    source_type: str
    created_at: str
    permissions: List[str] = field(default_factory=list)
    additional_info: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DocumentEmbedding:
    """
    Data model representing a vector embedding of a full document.
    """
    document_id: str
    tenant_id: str
    embedding: List[float]
    metadata: EmbeddingMetadata

@dataclass
class ChunkEmbedding:
    """
    Data model representing a vector embedding of an individual chunk.
    """
    chunk_id: str
    document_id: str
    tenant_id: str
    embedding: List[float]
    metadata: EmbeddingMetadata
