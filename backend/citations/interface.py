from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import Citation, SourceReference, ProvenanceMap

class ICitationService(ABC):
    """
    Interface for source tracking, citation generation, and provenance mapping.
    """

    @abstractmethod
    def track_sources(self, retrieved_chunks: List[Any], nodes: List[Any], edges: List[Any]) -> List[SourceReference]:
        """Convert input data objects into standard tracking items."""
        pass

    @abstractmethod
    def generate_citations(self, answer: str, references: List[SourceReference]) -> List[Citation]:
        """Align generated text fragments back to referenced sources."""
        pass

    @abstractmethod
    def build_provenance(self, references: List[SourceReference], doc_metadata: Dict[str, Any]) -> ProvenanceMap:
        """Create mapping representing relationships between graphs and documents."""
        pass

    @abstractmethod
    def validate_citations(self, citations: List[Citation], answer: str) -> bool:
        """Check citations for validity, ensuring target text boundaries exist."""
        pass
