from abc import ABC, abstractmethod
from typing import List
from .models import GraphNode, GraphEdge

class IRelationshipExtractor(ABC):
    """
    Interface for discovering context relationships linking identified entities.
    """

    @abstractmethod
    def extract_relationships(self, text: str, nodes: List[GraphNode]) -> List[GraphEdge]:
        """Discover and build directed edges among identified nodes."""
        pass

class LLMRelationshipExtractor(IRelationshipExtractor):
    """
    Placeholder LLM-driven relation extraction coordinator.
    """
    def extract_relationships(self, text: str, nodes: List[GraphNode]) -> List[GraphEdge]:
        # Placeholder mock list
        return []
