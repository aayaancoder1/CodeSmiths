from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import GraphNode, GraphEdge, GraphDelta

class IGraphConstructionService(ABC):
    """
    Interface for extracting, parsing, and storing entities and relationships.
    """

    @abstractmethod
    def extract_entities(self, text: str) -> List[GraphNode]:
        """Perform text parsing to discover structural entity nodes."""
        pass

    @abstractmethod
    def extract_relationships(self, text: str, nodes: List[GraphNode]) -> List[GraphEdge]:
        """Discover directed semantic connections between structural nodes."""
        pass

    @abstractmethod
    def create_nodes(self, nodes: List[GraphNode]) -> None:
        """Insert nodes into database storage."""
        pass

    @abstractmethod
    def create_edges(self, edges: List[GraphEdge]) -> None:
        """Insert edges into database storage."""
        pass

    @abstractmethod
    def update_graph(self, delta: GraphDelta) -> None:
        """Apply batch additions, updates, and deletes to the graph database."""
        pass

    @abstractmethod
    def delete_graph_objects(self, node_ids: List[str], edge_ids: List[str]) -> None:
        """Remove specified nodes and edges from storage."""
        pass
