import os
from backend.embeddings.provider import SentenceTransformerProvider
from backend.embeddings.service import EmbeddingService
from backend.embeddings.qdrant_client import QdrantClientAdapter
from backend.graph.neo4j_adapter import Neo4jAdapter
from backend.rag.graph_expander import GraphContextExpander

def main():
    print("1. Initializing providers and adapters...")
    provider = SentenceTransformerProvider()
    
    # Qdrant Client Adapter
    qdrant_client = QdrantClientAdapter(url="http://localhost:6333")
    service = EmbeddingService(provider=provider, qdrant_client=qdrant_client)
    
    # Neo4j Adapter
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password123")
    neo4j_adapter = Neo4jAdapter(uri=uri, user=user, password=password)
    
    print("2. Connecting to databases...")
    neo4j_adapter.connect()
    
    # Ensure Neo4j demo graph is populated
    print("Ensuring Neo4j graph is populated for the test...")
    with neo4j_adapter.driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    neo4j_adapter.create_node(label="Service", node_id="Payment Service", properties={"status": "degraded"})
    neo4j_adapter.create_node(label="Incident", node_id="Incident #1001", properties={"severity": "critical", "description": "Payment outage"})
    neo4j_adapter.create_node(label="Document", node_id="Slack Thread", properties={"channel": "incident-response"})
    neo4j_adapter.create_node(label="Service", node_id="Redis Cluster", properties={"role": "cache"})
    
    neo4j_adapter.create_relationship(source_id="Payment Service", target_id="Incident #1001", rel_type="CAUSED")
    neo4j_adapter.create_relationship(source_id="Incident #1001", target_id="Slack Thread", rel_type="DISCUSSED_IN")
    neo4j_adapter.create_relationship(source_id="Slack Thread", target_id="Redis Cluster", rel_type="REFERENCES")
    
    # Ensure Qdrant has embeddings (though test_qdrant already did, let's just use existing collection 'company_brain_demo' or recreate if needed)
    collection_name = "company_brain_demo"
    if not qdrant_client.collection_exists(collection_name):
        print("Collection 'company_brain_demo' not found. Please run test_qdrant.py first!")
        return

    # 3. Query Qdrant for "payment outage"
    query_text = "payment outage"
    print(f"\n3. Querying Qdrant for: '{query_text}'...")
    query_vector = service.embed_query(query_text)
    retrieved_docs = qdrant_client.search_embeddings(
        collection_name=collection_name,
        query_vector=query_vector,
        tenant_id="tenant-123",
        top_k=3
    )

    print("\n--- Retrieved Documents ---")
    for doc in retrieved_docs:
        print(f"- Doc ID: {doc.get('document_id')} | Score: {doc.get('score'):.4f}")

    # 4. Expand graph neighbors
    print("\n4. Expanding graph context based on retrieved documents...")
    expander = GraphContextExpander(neo4j_adapter=neo4j_adapter)
    expanded_context = expander.build_graph_context(retrieved_docs=retrieved_docs, tenant_id="tenant-123")

    # 5. Print Discovered Entities and Relationships
    print("\n--- Discovered Entities ---")
    for entity in expanded_context.entities:
        print(f"[{entity['label']}] ID: {entity['node_id']} | Props: {entity['properties']}")

    print("\n--- Discovered Relationships ---")
    for rel in expanded_context.relationships:
        print(f"({rel['source_id']}) -[{rel['type']}]-> ({rel['target_id']})")

    print("\n--- Serialized Graph Context ---")
    serialized = expander.serialize_graph_context(expanded_context)
    print(serialized)

    # 6. Verify correct expansion
    print("\nVerifying expansion correctness...")
    entity_ids = [e["node_id"] for e in expanded_context.entities]
    expected_entities = ["Payment Service", "Incident #1001", "Slack Thread", "Redis Cluster"]
    for expected in expected_entities:
        assert expected in entity_ids, f"Expected entity '{expected}' to be in the expanded context!"
    print("SUCCESS: Graph expansion verified successfully!")

    neo4j_adapter.close()

if __name__ == "__main__":
    main()
