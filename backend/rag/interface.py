from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import RagRequest, RagResponse, AssembledContext, ExpandedGraphContext, RagPrompt

class IGraphRagService(ABC):
    """
    Interface for running Graph-Augmented RAG execution pipelines.
    """

    @abstractmethod
    def build_context(self, chunks: List[Dict[str, Any]], graph_context: ExpandedGraphContext) -> AssembledContext:
        """Assembles textual chunks and graph data pools."""
        pass

    @abstractmethod
    def expand_graph(self, seed_nodes: List[Dict[str, Any]], tenant_id: str) -> ExpandedGraphContext:
        """Query Neo4j neighborhoods to retrieve relational entity networks."""
        pass

    @abstractmethod
    def construct_prompt(self, context: AssembledContext, query: str) -> RagPrompt:
        """Assemble structured system/user instructions for models."""
        pass

    @abstractmethod
    def synthesize_answer(self, prompt: RagPrompt) -> str:
        """Send formatted contexts to model APIs to obtain text synthesis."""
        pass

    @abstractmethod
    def run_graph_rag(self, request: RagRequest, retrieved_chunks: List[Dict[str, Any]], seed_nodes: List[Dict[str, Any]]) -> RagResponse:
        """Coordinate the query processing flow from beginning to end."""
        pass
