from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IGraphService(ABC):
    """
    Interface for the Knowledge Graph and Graph Traversal Service.
    Handles entity and relation extraction, updates, and multi-hop neighborhood expansion/traversal.
    """

    @abstractmethod
    def extract_and_update(self, text: str, document_id: str) -> None:
        """Extract entities/relationships from text and update Neo4j."""
        pass

    @abstractmethod
    def expand_neighborhood(self, seed_entities: List[str], max_depth: int = 2) -> Dict[str, Any]:
        """Perform graph traversal/neighborhood expansion for query reasoning context."""
        pass
