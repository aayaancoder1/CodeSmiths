from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import BrainDocument, BrainQuery, BrainOutput

class IBrainIntegrationService(ABC):
    """
    Unified entry-point interface for the AI Company Brain intelligence layer.
    """

    @abstractmethod
    def ingest_document(self, doc: BrainDocument) -> None:
        """Process document parsing, embedding pipelines, and graph index extraction."""
        pass

    @abstractmethod
    def retrieve_context(self, query: BrainQuery) -> Any:
        """Execute parallel lexical and semantic search queries."""
        pass

    @abstractmethod
    def expand_graph(self, seed_nodes: List[Any], tenant_id: str) -> Any:
        """Perform Neo4j path traversals around seed entities."""
        pass

    @abstractmethod
    def run_graph_rag(self, query: BrainQuery) -> Any:
        """Synthesize final responses from combined search contexts and relation networks."""
        pass

    @abstractmethod
    def generate_citations(self, answer: str, context: Any) -> Any:
        """Derive token span attributions mapping back to documents/nodes."""
        pass

    @abstractmethod
    def evaluate_answer(self, response: Any, ground_truth: Any = None) -> Any:
        """Run faithfulness, completeness, and latency metrics validation checks."""
        pass

    @abstractmethod
    def execute_pipeline(self, query: BrainQuery) -> BrainOutput:
        """Run the comprehensive query retrieval lifecycle workflow."""
        pass
