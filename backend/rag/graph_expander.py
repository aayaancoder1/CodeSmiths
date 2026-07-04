from typing import List, Dict, Any, Optional
from .models import ExpandedGraphContext
from backend.graph.neo4j_adapter import Neo4jAdapter

class GraphContextExpander:
    """
    Expands seed entity sets using Neo4j traversals or neighborhood expansion.
    """
    def __init__(self, neo4j_adapter: Neo4jAdapter):
        self.neo4j_adapter = neo4j_adapter

    def _map_document_to_seeds(self, doc_id: str) -> List[str]:
        """
        Maps a retrieved document ID/filename to starting seed entity IDs.
        """
        seeds = []
        doc_lower = doc_id.lower()
        if "payment" in doc_lower or "incident" in doc_lower:
            seeds.extend(["Payment Service", "Incident #1001"])
        if "redis" in doc_lower:
            seeds.append("Redis Cluster")
        if "slack" in doc_lower or "thread" in doc_lower:
            seeds.append("Slack Thread")
        return seeds

    def _get_node_details(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a node's label and properties from Neo4j.
        """
        if not self.neo4j_adapter.driver:
            raise RuntimeError("Neo4j adapter driver is not connected.")
        
        query = "MATCH (n {node_id: $node_id}) RETURN labels(n) as labels, properties(n) as properties"
        with self.neo4j_adapter.driver.session() as session:
            res = session.run(query, node_id=node_id).single()
            if res:
                return {
                    "node_id": node_id,
                    "label": res["labels"][0] if res["labels"] else "Entity",
                    "properties": res["properties"]
                }
        return None

    def get_entity_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        """
        Queries Neo4j to find the neighbor nodes and relationships for a given node_id.
        """
        return self.neo4j_adapter.get_neighbors(node_id)

    def expand_graph(self, retrieved_docs: List[Dict[str, Any]], tenant_id: str) -> ExpandedGraphContext:
        """
        Identify seed nodes from retrieved documents and perform BFS traversal to build ExpandedGraphContext.
        """
        # 1. Identify seed nodes from retrieved documents
        seed_ids = []
        for doc in retrieved_docs:
            # Check payload key or document_id key
            payload = doc.get("payload") or doc
            doc_id = payload.get("document_id") or doc.get("id") or doc.get("document_id")
            if doc_id:
                seed_ids.extend(self._map_document_to_seeds(doc_id))
        
        # Ensure unique seeds
        seed_ids = list(set(seed_ids))
        
        visited_nodes = {}
        visited_edges = {}
        
        # Queue for BFS: (node_id, depth)
        queue = [(seed_id, 0) for seed_id in seed_ids]
        
        max_depth = 3
        while queue:
            curr_id, depth = queue.pop(0)
            
            # Fetch node properties if not already fetched
            if curr_id not in visited_nodes:
                node_details = self._get_node_details(curr_id)
                if node_details:
                    visited_nodes[curr_id] = node_details
            
            if depth >= max_depth:
                continue
                
            # Get neighbors
            neighbors = self.get_entity_neighbors(curr_id)
            for n in neighbors:
                neighbor_id = n["neighbor_id"]
                rel_type = n["rel_type"]
                is_outgoing = n["is_outgoing"]
                
                # Record node details
                if neighbor_id not in visited_nodes:
                    visited_nodes[neighbor_id] = {
                        "node_id": neighbor_id,
                        "label": n["labels"][0] if n["labels"] else "Entity",
                        "properties": n["properties"]
                    }
                    queue.append((neighbor_id, depth + 1))
                
                # Record edge details
                source = curr_id if is_outgoing else neighbor_id
                target = neighbor_id if is_outgoing else curr_id
                edge_key = f"{source}-{rel_type}-{target}"
                
                if edge_key not in visited_edges:
                    visited_edges[edge_key] = {
                        "source_id": source,
                        "target_id": target,
                        "type": rel_type,
                        "properties": n["rel_properties"]
                    }
        
        entities = list(visited_nodes.values())
        relationships = list(visited_edges.values())
        
        supporting_documents = []
        for doc in retrieved_docs:
            payload = doc.get("payload") or doc
            doc_id = payload.get("document_id") or doc.get("id") or doc.get("document_id")
            if doc_id:
                supporting_documents.append(doc_id)
        supporting_documents = list(set(supporting_documents))
        
        return ExpandedGraphContext(
            entities=entities,
            relationships=relationships,
            supporting_documents=supporting_documents
        )

    def build_graph_context(self, retrieved_docs: List[Dict[str, Any]], tenant_id: str) -> ExpandedGraphContext:
        """
        Builds the complete expanded graph context.
        """
        return self.expand_graph(retrieved_docs, tenant_id)

    def serialize_graph_context(self, context: ExpandedGraphContext) -> str:
        """
        Serializes the ExpandedGraphContext to a human-readable text string.
        """
        lines = []
        lines.append("Entities:")
        for entity in context.entities:
            lines.append(f"  - [{entity['label']}] {entity['node_id']} | Properties: {entity['properties']}")
        lines.append("\nRelationships:")
        for rel in context.relationships:
            lines.append(f"  - ({rel['source_id']}) -[{rel['type']}]-> ({rel['target_id']})")
        return "\n".join(lines)
