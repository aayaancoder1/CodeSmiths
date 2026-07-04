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

    # Ensure Neo4j graph is populated for the test
    print("Populating/Ensuring Neo4j graph is present...")
    with neo4j_adapter.driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    neo4j_adapter.create_node(label="Service", node_id="Payment Service", properties={"status": "degraded"})
    neo4j_adapter.create_node(label="Incident", node_id="Incident #1001", properties={"severity": "critical", "description": "Payment outage"})
    neo4j_adapter.create_node(label="Document", node_id="Slack Thread", properties={"channel": "incident-response"})
    neo4j_adapter.create_node(label="Service", node_id="Redis Cluster", properties={"role": "cache"})
    
    neo4j_adapter.create_relationship(source_id="Payment Service", target_id="Incident #1001", rel_type="CAUSED")
    neo4j_adapter.create_relationship(source_id="Incident #1001", target_id="Slack Thread", rel_type="DISCUSSED_IN")
    neo4j_adapter.create_relationship(source_id="Slack Thread", target_id="Redis Cluster", rel_type="REFERENCES")

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

    # 1. Query Qdrant
    query = "What caused the payment outage?"
    print(f"\n2. Retrieving documents from Qdrant for: '{query}'...")
    query_vector = embedding_service.embed_query(query)
    retrieved_docs = qdrant_client.search_embeddings(
        collection_name="company_brain_demo",
        query_vector=query_vector,
        tenant_id="tenant-123",
        top_k=3
    )

    print(f"Retrieved {len(retrieved_docs)} documents.")

    # Execute graph expansion and generation via orchestrated RAG service pipeline
    request = RagRequest(query=query, tenant_id="tenant-123")
    
    print("\n3. Executing Graph RAG generation pipeline...")
    response = rag_service.run_graph_rag(
        request=request,
        retrieved_chunks=retrieved_docs,
        seed_nodes=[] # Inferred from retrieved documents
    )

    print("\n--- Final Answer ---")
    print(response.answer)
    print("--------------------")

    print("\n--- Supporting Documents ---")
    for doc in response.context.graph_context.supporting_documents:
        print(f"- {doc}")

    print("\n--- Supporting Entities ---")
    for entity in response.context.graph_context.entities:
        print(f"- [{entity['label']}] {entity['node_id']}")

    print("\nSUCCESS: Graph RAG Pipeline executed successfully!")
    neo4j_adapter.close()

if __name__ == "__main__":
    main()
