import os
from backend.embeddings.provider import SentenceTransformerProvider
from backend.embeddings.service import EmbeddingService
from backend.embeddings.qdrant_client import QdrantClientAdapter
from backend.graph.neo4j_adapter import Neo4jAdapter
from backend.rag.graph_expander import GraphContextExpander
from backend.rag.context_builder import ContextBuilder
from backend.rag.prompt_builder import PromptBuilder
from backend.rag.synthesis import SynthesisService
from backend.rag.orchestrator import RagOrchestrator
from backend.rag.service import RagService
from backend.rag.models import RagRequest

# Citation imports
from backend.citations.source_tracker import SourceTracker
from backend.citations.citation_builder import CitationBuilder
from backend.citations.provenance import ProvenanceMapper
from backend.citations.service import CitationService

def main():
    print("1. Initializing providers and database connections...")
    provider = SentenceTransformerProvider()
    
    # Qdrant client adapter
    qdrant_client = QdrantClientAdapter(url="http://localhost:6333")
    embedding_service = EmbeddingService(provider=provider, qdrant_client=qdrant_client)
    
    # Neo4j adapter
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password123")
    neo4j_adapter = Neo4jAdapter(uri=uri, user=user, password=password)
    neo4j_adapter.connect()

    # Initialize Graph RAG Components
    expander = GraphContextExpander(neo4j_adapter=neo4j_adapter)
    builder = ContextBuilder()
    prompt_builder = PromptBuilder()
    synthesis = SynthesisService()
    
    orchestrator = RagOrchestrator(
        expander=expander,
        builder=builder,
        prompt_builder=prompt_builder,
        synthesis=synthesis
    )
    rag_service = RagService(orchestrator=orchestrator)

    # Initialize Citation components
    tracker = SourceTracker()
    cit_builder = CitationBuilder()
    mapper = ProvenanceMapper()
    citation_service = CitationService(tracker=tracker, builder=cit_builder, mapper=mapper)

    # 1. Run Graph RAG pipeline
    query = "What caused the payment outage?"
    print(f"\n2. Executing RAG retrieval and synthesis for: '{query}'...")
    query_vector = embedding_service.embed_query(query)
    retrieved_docs = qdrant_client.search_embeddings(
        collection_name="company_brain_demo",
        query_vector=query_vector,
        tenant_id="tenant-123",
        top_k=3
    )

    request = RagRequest(query=query, tenant_id="tenant-123")
    response = rag_service.run_graph_rag(
        request=request,
        retrieved_chunks=retrieved_docs,
        seed_nodes=[]
    )

    # 2. Collect retrieved documents and graph expansion results
    graph_context = response.context.graph_context
    retrieved_chunks = response.context.retrieved_chunks
    
    print("\n3. Tracking sources and building citations...")
    # 3. Track sources
    references = citation_service.track_sources(
        retrieved_chunks=retrieved_chunks,
        nodes=graph_context.entities,
        edges=graph_context.relationships
    )

    # 4. Generate citations
    citations = citation_service.generate_citations(
        answer=response.answer,
        references=references
    )

    # 5. Format and print final answer with sources
    print("\n--- Final formatted output ---")
    formatted_output = citation_service.format_answer_with_sources(
        answer=response.answer,
        citations=citations
    )
    print(formatted_output)
    print("------------------------------")

    # Assertions to verify correctness
    assert len(citations) > 0, "No citations generated!"
    assert len(retrieved_chunks) > 0, "No documents retrieved!"
    print("SUCCESS: Citation Pipeline execution verified successfully!")
    
    neo4j_adapter.close()

if __name__ == "__main__":
    main()
