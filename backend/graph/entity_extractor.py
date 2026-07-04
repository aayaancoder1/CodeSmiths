from abc import ABC, abstractmethod
from typing import List
from .models import GraphNode

class IEntityExtractor(ABC):
    """
    Interface for parsing text contents and identifying domain entity nodes.
    """

    @abstractmethod
    def extract_entities(self, text: str) -> List[GraphNode]:
        """Extract and structure GraphNodes found in raw source text."""
        pass

class LLMEntityExtractor(IEntityExtractor):
    """
    Placeholder LLM-driven entity extraction coordinator.
    """
    def extract_entities(self, text: str) -> List[GraphNode]:
        # Placeholder mock list
        return []
