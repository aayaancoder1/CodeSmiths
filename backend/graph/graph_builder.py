from typing import List
from .models import GraphNode, GraphEdge, GraphDelta

class GraphBuilder:
    """
    Compiles separate entity and relationship extraction outcomes into a unified GraphDelta.
    """

    def build_delta(self, nodes: List[GraphNode], edges: List[GraphEdge]) -> GraphDelta:
        # Placeholder builder formatting logic
        return GraphDelta(
            nodes_to_upsert=nodes,
            edges_to_upsert=edges
        )
