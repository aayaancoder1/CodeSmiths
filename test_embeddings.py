import os
from backend.embeddings.provider import SentenceTransformerProvider
from backend.embeddings.service import EmbeddingService
from backend.embeddings.models import EmbeddingMetadata

def main():
    print("Initializing SentenceTransformer Embedding Provider...")
    provider = SentenceTransformerProvider()
    service = EmbeddingService(provider=provider)

    data_dir = "data/demo_documents"
    demo_files = ["payment_incident.md", "redis_outage.md", "slack_thread.md"]

    for filename in demo_files:
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"\nProcessing File: {filename} ({len(text)} chars)")
        metadata = EmbeddingMetadata(
            source_type="markdown",
            created_at="2026-07-04T12:00:00Z",
            permissions=["eng", "admin"]
        )

        doc_emb = service.generate_document_embeddings(
            document_id=filename,
            tenant_id="tenant-123",
            text=text,
            metadata=metadata
        )

        print(f"-> Generated Document Embedding Dimension: {len(doc_emb.embedding)}")
        print(f"-> Embedding values head (first 5 dimensions): {doc_emb.embedding[:5]}")

        # Test chunking generation on raw text chunks
        chunk_text = text.split("\n\n")[0]
        chunk_emb = service.generate_chunk_embeddings(
            document_id=filename,
            chunk_id=f"{filename}_chunk_0",
            tenant_id="tenant-123",
            text=chunk_text,
            metadata=metadata
        )
        print(f"-> Generated Chunk Embedding Dimension: {len(chunk_emb.embedding)}")
        print(f"-> Chunk text: {repr(chunk_text)}")

if __name__ == "__main__":
    main()
