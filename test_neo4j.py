import os
from backend.graph.neo4j_adapter import Neo4jAdapter

def main():
    print("Connecting to Neo4j database...")
    # Get credentials from environment or use defaults
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password123")
    
    adapter = Neo4jAdapter(uri=uri, user=user, password=password)
    try:
        adapter.connect()
        print("Connected successfully!")
    except Exception as e:
        print(f"Failed to connect to Neo4j at {uri}: {e}")
        print("Please make sure Neo4j is running locally.")
        return

    try:
        # Clear existing nodes/edges to make the test idempotent
        print("Clearing existing database elements...")
        with adapter.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

        # 1. Create nodes
        print("\nCreating nodes...")
        adapter.create_node(label="Service", node_id="Payment Service", properties={"status": "degraded"})
        adapter.create_node(label="Incident", node_id="Incident #1001", properties={"severity": "critical", "description": "Payment outage"})
        adapter.create_node(label="Document", node_id="Slack Thread", properties={"channel": "incident-response"})
        adapter.create_node(label="Service", node_id="Redis Cluster", properties={"role": "cache"})

        # 2. Create relationships
        print("Creating relationships...")
        adapter.create_relationship(source_id="Payment Service", target_id="Incident #1001", rel_type="CAUSED")
        adapter.create_relationship(source_id="Incident #1001", target_id="Slack Thread", rel_type="DISCUSSED_IN")
        adapter.create_relationship(source_id="Slack Thread", target_id="Redis Cluster", rel_type="REFERENCES")

        # 3. Verify node creation and retrieval
        print("\nVerifying node creation...")
        with adapter.driver.session() as session:
            res = session.run("MATCH (n) RETURN count(n) as count").single()
            node_count = res["count"]
            print(f"Total nodes created: {node_count}")
            assert node_count == 4, f"Expected 4 nodes, got {node_count}"

        # 4. Verify relationship creation
        print("Verifying relationship creation...")
        with adapter.driver.session() as session:
            res = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()
            rel_count = res["count"]
            print(f"Total relationships created: {rel_count}")
            assert rel_count == 3, f"Expected 3 relationships, got {rel_count}"

        # 5. Verify graph traversal
        print("\nVerifying graph traversal...")
        neighbors_payment = adapter.get_neighbors("Payment Service")
        print(f"Neighbors of 'Payment Service': {neighbors_payment}")
        assert len(neighbors_payment) > 0, "Payment Service has no neighbors!"
        
        # Multihop traversal check: Payment Service -> Incident #1001 -> Slack Thread -> Redis Cluster
        with adapter.driver.session() as session:
            query = (
                "MATCH p = (a {node_id: 'Payment Service'})-[:CAUSED]->"
                "(b {node_id: 'Incident #1001'})-[:DISCUSSED_IN]->"
                "(c {node_id: 'Slack Thread'})-[:REFERENCES]->"
                "(d {node_id: 'Redis Cluster'}) "
                "RETURN count(p) as path_count"
            )
            path_count = session.run(query).single()["path_count"]
            print(f"Verified multi-hop path exists: {path_count == 1}")
            assert path_count == 1, "Expected path from Payment Service to Redis Cluster not found!"

        # 6. Print all nodes and relationships
        print("\n--- Current Knowledge Graph state ---")
        print("Nodes:")
        with adapter.driver.session() as session:
            result = session.run("MATCH (n) RETURN labels(n) as labels, n.node_id as id, properties(n) as props")
            for record in result:
                print(f"  - [{record['labels'][0]}] ID: {record['id']} | Properties: {record['props']}")

        print("\nRelationships:")
        with adapter.driver.session() as session:
            result = session.run("MATCH (a)-[r]->(b) RETURN a.node_id as source, type(r) as type, b.node_id as target, properties(r) as props")
            for record in result:
                print(f"  - ({record['source']}) -[{record['type']}]-> ({record['target']})")
        print("--------------------------------------")

        print("\nSUCCESS: Neo4j Integration Validation PASSED!")

    finally:
        adapter.close()

if __name__ == "__main__":
    main()
