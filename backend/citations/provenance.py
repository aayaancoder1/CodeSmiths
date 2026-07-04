from typing import List, Dict, Any
from .models import ProvenanceMap, SourceReference

class ProvenanceMapper:
    """
    Constructs lineage mappings illustrating how structured entities link to documents.
    """

    def map_provenance(self, references: List[SourceReference], doc_metadata: Dict[str, Any]) -> ProvenanceMap:
        nodes = []
        edges = []
        
        docs = [ref for ref in references if ref.type == "document"]
        graph_nodes = [ref for ref in references if ref.type == "graph_node"]
        
        # Link graph nodes to documents based on name patterns
        for node in graph_nodes:
            node_id = node.source_id
            linked_docs = []
            
            for doc in docs:
                doc_id = doc.source_id
                # Heuristic mapping for the demo incident path
                if "payment" in node_id.lower() and "payment" in doc_id.lower():
                    linked_docs.append(doc_id)
                elif "redis" in node_id.lower() and "redis" in doc_id.lower():
                    linked_docs.append(doc_id)
                elif "slack" in node_id.lower() and "slack" in doc_id.lower():
                    linked_docs.append(doc_id)
            
            nodes.append({
                "entity_id": node_id,
                "type": node.metadata.get("label", "Entity"),
                "provenance_sources": linked_docs
            })
            
        return ProvenanceMap(nodes=nodes, edges=edges)
