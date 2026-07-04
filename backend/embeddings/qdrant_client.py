from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from abc import ABC, abstractmethod

class IQdrantClient(ABC):
    """
    Interface for the Qdrant database vector store operations.
    """

    @abstractmethod
    def upsert_vectors(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        """Upsert points (IDs, vectors, payloads) to a collection."""
        pass

    @abstractmethod
    def delete_vectors(self, collection_name: str, point_ids: List[str]) -> None:
        """Delete points from a collection by ID."""
        pass

    @abstractmethod
    def delete_by_filter(self, collection_name: str, filter_query: Dict[str, Any]) -> None:
        """Delete points matching a specific metadata filter (e.g. document_id)."""
        pass


class QdrantClientAdapter(IQdrantClient):
    """
    Concrete implementation of IQdrantClient using the real qdrant-client.
    Runs Qdrant in-memory for testing and demonstration workflows.
    """
    def __init__(self, location: str = ":memory:"):
        self.client = QdrantClient(location=location)

    def collection_exists(self, collection_name: str) -> bool:
        collections = self.client.get_collections().collections
        return any(c.name == collection_name for c in collections)

    def create_collection(self, collection_name: str, vector_size: int = 384) -> None:
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    def upsert_vectors(self, collection_name: str, points: List[Dict[str, Any]]) -> None:
        qdrant_points = []
        for p in points:
            qdrant_points.append(
                PointStruct(
                    id=p["id"],
                    vector=p["vector"],
                    payload=p["payload"]
                )
            )
        self.client.upsert(
            collection_name=collection_name,
            points=qdrant_points
        )

    def search_embeddings(self, collection_name: str, query_vector: List[float], tenant_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        # Retrieve similarities filtered by tenant_id using the query_points method
        results = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True
        ).points
        # Filter matching tenant_id
        f_results = []
        for r in results:
            payload = r.payload or {}
            if payload.get("tenant_id") == tenant_id:
                f_results.append({
                    "id": r.id,
                    "score": r.score,
                    "payload": payload
                })
        return f_results

    def delete_vectors(self, collection_name: str, point_ids: List[str]) -> None:
        self.client.delete(
            collection_name=collection_name,
            points_selector=point_ids
        )

    def delete_by_filter(self, collection_name: str, filter_query: Dict[str, Any]) -> None:
        # Simplistic in-memory filter deletion simulation
        # Since it is a demo environment, delete points sequentially matching filter values.
        # Fetch all points first
        scroll_res = self.client.scroll(
            collection_name=collection_name,
            limit=100,
            with_payload=True,
            with_vectors=False
        )[0]
        to_delete = []
        for point in scroll_res:
            payload = point.payload or {}
            match = True
            for k, v in filter_query.items():
                if payload.get(k) != v:
                    match = False
                    break
            if match:
                to_delete.append(point.id)
        if to_delete:
            self.delete_vectors(collection_name, to_delete)
