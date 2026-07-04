from typing import List, Dict, Any
from .models import SourceReference

class SourceTracker:
    """
    Registers and tracks retrieved documents, chunks, and graph objects
    used throughout query evaluation.
    """

    def track(self, chunks: List[Dict[str, Any]], nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[SourceReference]:
        refs = []
        
        # Convert Qdrant chunk/document records into standard references
        for chk in chunks:
            payload = chk.get("payload") or chk
            doc_id = payload.get("document_id") or chk.get("id") or "Unknown"
            refs.append(SourceReference(
                source_id=doc_id,
                type="document",
                metadata={"score": chk.get("score", 1.0), "payload": payload}
            ))
            
        # Convert Neo4j graph nodes into standard references
        for nd in nodes:
            refs.append(SourceReference(
                source_id=nd.get("node_id", "Unknown"),
                type="graph_node",
                metadata=nd
            ))
            
        # Convert Neo4j relationships into standard references
        for ed in edges:
            refs.append(SourceReference(
                source_id=f"{ed.get('source_id')}-{ed.get('type')}-{ed.get('target_id')}",
                type="graph_edge",
                metadata=ed
            ))
            
        return refs
