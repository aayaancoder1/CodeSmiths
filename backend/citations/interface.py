from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ICitationService(ABC):
    """
    Interface for the Citation Service.
    Tracks sources used in RAG responses and attributes them accurately.
    """

    @abstractmethod
    def generate_citations(self, answer: str, source_contexts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Maps synthesized answers back to original chunk sources to generate clean citations."""
        pass
