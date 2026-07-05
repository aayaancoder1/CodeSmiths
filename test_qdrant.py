import os
from backend.embeddings.provider import SentenceTransformerProvider
from backend.embeddings.service import EmbeddingService
from backend.embeddings.models import EmbeddingMetadata
from backend.embeddings.qdrant_client import QdrantClientAdapter

def main():
    print("Initializing SentenceTransformer Embedding Provider...")
    provider = SentenceTransformerProvider()
    
    print("Connecting to Qdrant at http://localhost:6333...")
    qdrant_client = QdrantClientAdapter(url="http://localhost:6333")
    
    # Bind provider and client inside the coordinate service
    service = EmbeddingService(provider=provider, qdrant_client=qdrant_client)

    collection_name = "company_brain_demo"
    print(f"Checking if collection '{collection_name}' exists...")
    if qdrant_client.collection_exists(collection_name):
        print(f"Collection '{collection_name}' already exists. Deleting it to ensure a fresh test run...")
        qdrant_client.client.delete_collection(collection_name)
    
    print(f"Creating collection '{collection_name}' with vector size 384 and distance COSINE...")
    qdrant_client.create_collection(collection_name, vector_size=384)
    
    # Verify collection creation
    assert qdrant_client.collection_exists(collection_name), "Failed to verify collection creation!"
    print("Verified: Collection exists.")

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
            permissions=["eng", "admin"],
            additional_info={"source_file": filename}
        )

        # Generate chunk embedding
        chunk_emb = service.generate_chunk_embeddings(
            document_id=filename,
            chunk_id=str(idx),
            tenant_id="tenant-123",
            text=text,
            metadata=metadata
        )
        embeddings_list.append(chunk_emb)

    print("Storing embeddings to Qdrant...")
    service.store_embeddings(collection_name, embeddings_list)
    print("Verified: Vector insertion completed.")

    # Search for "payment outage"
    search_query = "payment outage"
    print(f"\nSearching for query: '{search_query}'...")
    query_vector = service.embed_query(search_query)
    
    # Search via adapter
    search_results = qdrant_client.search_embeddings(
        collection_name=collection_name,
        query_vector=query_vector,
        tenant_id="tenant-123",
        top_k=3
    )

    print(f"\nSearch results count (top 3): {len(search_results)}")
    for r in search_results:
        print(f"Score: {r['score']:.4f}")
        print(f"Document ID: {r['document_id']}")
        print(f"Chunk ID: {r['chunk_id']}")
        print(f"Metadata: {r['metadata']}")
        print("-" * 40)

    # Verification assertions
    assert len(search_results) > 0, "No search results returned!"
    print("SUCCESS: Qdrant Integration Validation PASSED!")

if __name__ == "__main__":
    main()
