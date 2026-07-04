import os
from backend.embeddings.provider import SentenceTransformerProvider
from backend.embeddings.service import EmbeddingService
from backend.embeddings.models import EmbeddingMetadata
from backend.embeddings.qdrant_client import QdrantClientAdapter

def main():
    print("Initializing SentenceTransformer Embedding Provider...")
    provider = SentenceTransformerProvider()
    
    print("Initializing Qdrant Memory Client Adapter...")
    qdrant_client = QdrantClientAdapter(location=":memory:")
    
    # Bind provider and client inside the coordinate service
    service = EmbeddingService(provider=provider, qdrant_client=qdrant_client)

    collection_name = "demo_chunks"
    print(f"Creating collection '{collection_name}'...")
    qdrant_client.create_collection(collection_name, vector_size=384)

    data_dir = "data/demo_documents"
    demo_files = ["payment_incident.md", "redis_outage.md", "slack_thread.md"]
    embeddings_list = []

    for idx, filename in enumerate(demo_files):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"Generating embeddings for document: {filename}...")
        metadata = EmbeddingMetadata(
            source_type="markdown",
            created_at="2026-07-04T12:00:00Z",
            permissions=["eng", "admin"]
        )

        # Generate chunk embedding
        chunk_emb = service.generate_chunk_embeddings(
            document_id=filename,
            chunk_id=idx,
            tenant_id="tenant-123",
            text=text,
            metadata=metadata
        )
        embeddings_list.append(chunk_emb)

    print("Storing embeddings to Qdrant...")
    service.store_embeddings(collection_name, embeddings_list)

    print("\nRetrieving Top 3 matched embeddings for search query: 'outage session tokens failed'...")
    query_vector = service.embed_query("outage session tokens failed")
    
    # Search via adapter directly (tenancy isolation check)
    search_results = qdrant_client.search_embeddings(
        collection_name=collection_name,
        query_vector=query_vector,
        tenant_id="tenant-123",
        top_k=3
    )

    print(f"\nSearch results count: {len(search_results)}")
    for r in search_results:
        print(f"-> Match ID: {r['id']}, Score: {r['score']:.4f}")
        print(f"   Payload: {r['payload']}")

    # Validation assertions
    assert len(search_results) > 0, "No search results returned!"
    # The top result should be the redis outage because the query matches "outage session tokens"
    top_result_doc = search_results[0]['payload']['document_id']
    print(f"\nTop Result Document Match: {top_result_doc}")
    assert top_result_doc == "redis_outage.md", f"Expected redis_outage.md, but got {top_result_doc}"
    print("SUCCESS: Qdrant Integration Validation PASSED!")

if __name__ == "__main__":
    main()
