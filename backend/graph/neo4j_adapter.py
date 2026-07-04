import os
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
from .graph_storage import IGraphStorage
from .models import GraphNode, GraphEdge, GraphDelta

class Neo4jAdapter(IGraphStorage):
    """
    Adapter implementing graph mutations using Cypher statements or driver logic.
    """
    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        self.uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.environ.get("NEO4J_USER", "neo4j")
        self.password = password or os.environ.get("NEO4J_PASSWORD", "password123")
        self.driver = None

    def connect(self) -> None:
        """Establishes connection to the Neo4j instance."""
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        # Verify connection by running a quick query
        self.driver.verify_connectivity()

    def close(self) -> None:
        """Closes the database driver."""
        if self.driver:
            self.driver.close()

    def create_node(self, label: str, node_id: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """Creates a node in Neo4j with a specific label, ID and properties."""
        if not self.driver:
            raise RuntimeError("Driver not connected. Call connect() first.")
        
        props = properties.copy() if properties else {}
        props["node_id"] = node_id
        
        # Sanitize label (labels cannot be parameterized directly in Cypher)
        allowed_labels = {"Person", "Service", "Incident", "Document", "Ticket"}
        if label not in allowed_labels:
            raise ValueError(f"Invalid node label: {label}. Must be one of {allowed_labels}")

        query = f"MERGE (n:{label} {{node_id: $node_id}}) SET n += $props"
        with self.driver.session() as session:
            session.run(query, node_id=node_id, props=props)

    def create_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """Creates a directed relationship between two nodes by their IDs."""
        if not self.driver:
            raise RuntimeError("Driver not connected. Call connect() first.")
        
        allowed_rels = {"CAUSED", "DISCUSSED_IN", "REFERENCES", "WORKS_ON", "OWNS"}
        if rel_type not in allowed_rels:
            raise ValueError(f"Invalid relationship type: {rel_type}. Must be one of {allowed_rels}")

        props = properties or {}
        query = (
            f"MATCH (a {{node_id: $source_id}}), (b {{node_id: $target_id}}) "
            f"MERGE (a)-[r:{rel_type}]->(b) "
            f"SET r += $props"
        )
        with self.driver.session() as session:
            session.run(query, source_id=source_id, target_id=target_id, props=props)

    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        """Retrieve the neighborhood (nodes and edges) of a given node."""
        if not self.driver:
            raise RuntimeError("Driver not connected. Call connect() first.")
        
        query = (
            "MATCH (n {node_id: $node_id})-[r]-(m) "
            "RETURN labels(m) as labels, m.node_id as neighbor_id, properties(m) as properties, "
            "type(r) as rel_type, properties(r) as rel_properties, startNode(r) = n as is_outgoing"
        )
        
        neighbors = []
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            for record in result:
                neighbors.append({
                    "neighbor_id": record["neighbor_id"],
                    "labels": record["labels"],
                    "properties": record["properties"],
                    "rel_type": record["rel_type"],
                    "rel_properties": record["rel_properties"],
                    "is_outgoing": record["is_outgoing"]
                })
        return neighbors

    def delete_node(self, node_id: str) -> None:
        """Delete a node and all of its relationships."""
        if not self.driver:
            raise RuntimeError("Driver not connected. Call connect() first.")
        
        query = "MATCH (n {node_id: $node_id}) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query, node_id=node_id)

    # Implement IGraphStorage abstract methods for integration compatibility
    def add_nodes(self, nodes: List[GraphNode]) -> None:
        for node in nodes:
            self.create_node(label=node.label, node_id=node.node_id, properties=node.properties)

    def add_edges(self, edges: List[GraphEdge]) -> None:
        for edge in edges:
            self.create_relationship(source_id=edge.source_id, target_id=edge.target_id, rel_type=edge.type, properties=edge.properties)

    def apply_delta(self, delta: GraphDelta) -> None:
        self.add_nodes(delta.nodes_to_upsert)
        self.add_edges(delta.edges_to_upsert)
        for nid in delta.nodes_to_delete:
            self.delete_node(nid)

    def delete_elements(self, node_ids: List[str], edge_ids: List[str]) -> None:
        for nid in node_ids:
            self.delete_node(nid)
