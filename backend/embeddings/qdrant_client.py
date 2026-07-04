import uuid
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector
)
from abc import ABC, abstractmethod

class IQdrantClient(ABC):
    """
    Interface for the Qdrant database vector store operations.
    """

    @abstractmethod
    def create_collection(self, collection_name: str, vector_size: int = 384) -> None:
        """Create a collection in Qdrant."""
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in Qdrant."""
        pass

    @abstractmethod
    def store_embeddings(self, collection_name: str, embeddings: List[Any]) -> None:
        """Store generated embeddings to the Qdrant collection."""
        pass

    @abstractmethod
    def search_embeddings(
        self,
        collection_name: str,
        query_vector: List[float],
        tenant_id: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Search for top_k similar vectors with tenant isolation filter."""
        pass

    @abstractmethod
    def delete_embeddings(
        self,
        collection_name: str,
        document_id: Optional[str] = None,
        chunk_ids: Optional[List[str]] = None
    ) -> None:
        """Delete embeddings from the collection by document_id or explicit chunk_ids."""
        pass


def clean_point_id(id_val: Any) -> Any:
    """
    Ensure Qdrant point ID is a valid integer or UUID.
    If it's a string, try to parse it as UUID. If not, generate a deterministic UUID.
    """
    if isinstance(id_val, int):
        return id_val
    try:
        # Check if it's already a valid UUID string
        uuid.UUID(str(id_val))
        return str(id_val)
    except ValueError:
        # Generate a deterministic UUID from the string
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(id_val)))


class QdrantClientAdapter(IQdrantClient):
    """
    Concrete implementation of IQdrantClient using the real qdrant-client.
    Defaults to localhost:6333 for the real docker container.
    """
    def __init__(self, url: str = "http://localhost:6333"):
        self.client = QdrantClient(url=url)

    def collection_exists(self, collection_name: str) -> bool:
        collections = self.client.get_collections().collections
        return any(c.name == collection_name for c in collections)

    def create_collection(self, collection_name: str, vector_size: int = 384) -> None:
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    def store_embeddings(self, collection_name: str, embeddings: List[Any]) -> None:
        qdrant_points = []
        for emb in embeddings:
            raw_id = getattr(emb, "chunk_id", getattr(emb, "document_id", None))
            point_id = clean_point_id(raw_id)
            
            document_id = getattr(emb, "document_id", "")
            chunk_id = getattr(emb, "chunk_id", None)
            tenant_id = getattr(emb, "tenant_id", "")
            
            emb_metadata = getattr(emb, "metadata", None)
            source_type = ""
            metadata_dict = {}
            if emb_metadata:
                source_type = getattr(emb_metadata, "source_type", "")
                metadata_dict = {
                    "created_at": getattr(emb_metadata, "created_at", ""),
                    "permissions": getattr(emb_metadata, "permissions", []),
                    "additional_info": getattr(emb_metadata, "additional_info", {})
                }
            
            payload = {
                "document_id": document_id,
                "chunk_id": chunk_id,
                "tenant_id": tenant_id,
                "source_type": source_type,
                "metadata": metadata_dict
            }
            
            qdrant_points.append(
                PointStruct(
                    id=point_id,
                    vector=emb.embedding,
                    payload=payload
                )
            )
            
        self.client.upsert(
            collection_name=collection_name,
            points=qdrant_points
        )

    def search_embeddings(
        self,
        collection_name: str,
        query_vector: List[float],
        tenant_id: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        filter_cond = None
        if tenant_id:
            filter_cond = Filter(
                must=[
                    FieldCondition(
                        key="tenant_id",
                        match=MatchValue(value=tenant_id)
                    )
                ]
            )
        
        results = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=filter_cond,
            limit=top_k,
            with_payload=True
        ).points
        
        f_results = []
        for r in results:
            payload = r.payload or {}
            f_results.append({
                "id": r.id,
                "score": r.score,
                "document_id": payload.get("document_id"),
                "chunk_id": payload.get("chunk_id"),
                "tenant_id": payload.get("tenant_id"),
                "source_type": payload.get("source_type"),
                "metadata": payload.get("metadata", {}),
                "payload": payload  # maintaining compatibility with current tests
            })
        return f_results

    def delete_embeddings(
        self,
        collection_name: str,
        document_id: Optional[str] = None,
        chunk_ids: Optional[List[str]] = None
    ) -> None:
        if chunk_ids:
            cleaned_ids = [clean_point_id(cid) for cid in chunk_ids]
            self.client.delete(
                collection_name=collection_name,
                points_selector=cleaned_ids
            )
        elif document_id:
            self.client.delete(
                collection_name=collection_name,
                points_selector=FilterSelector(
                    filter=Filter(
                        must=[
                            FieldCondition(
                                key="document_id",
                                match=MatchValue(value=document_id)
                            )
                        ]
                    )
                )
            )
