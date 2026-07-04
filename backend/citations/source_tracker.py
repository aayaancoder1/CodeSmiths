from typing import List, Dict, Any
from .models import SourceReference

class SourceTracker:
    """
    Registers and tracks retrieved documents, chunks, and graph objects
    used throughout query evaluation.
    """

    def track(self, chunks: List[Dict[str, Any]], nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[SourceReference]:
        # Placeholder tracking mapper
        refs = []
        for chk in chunks:
            refs.append(SourceReference(source_id=chk.get("id", "chk_unknown"), type="chunk", metadata=chk))
        for nd in nodes:
            refs.append(SourceReference(source_id=nd.get("id", "nd_unknown"), type="graph_node", metadata=nd))
        return refs
