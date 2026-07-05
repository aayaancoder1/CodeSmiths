from abc import ABC, abstractmethod
from typing import List
from .models import GraphNode, GraphEdge, GraphDelta

class IGraphStorage(ABC):
    """
    Interface for mutating the underlying graph database (Neo4j).
    """

    @abstractmethod
    def add_nodes(self, nodes: List[GraphNode]) -> None:
        """Write nodes into the graph database."""
        pass

    @abstractmethod
    def add_edges(self, edges: List[GraphEdge]) -> None:
        """Write directed edges linking target nodes into the graph database."""
        pass

    @abstractmethod
    def apply_delta(self, delta: GraphDelta) -> None:
        """Execute delta batch mutations on the graph store."""
        pass

    @abstractmethod
    def delete_elements(self, node_ids: List[str], edge_ids: List[str]) -> None:
        """Purge specific nodes or edges from storage."""
        pass
