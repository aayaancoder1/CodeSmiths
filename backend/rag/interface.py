from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IRagService(ABC):
    """
    Interface for the Orchestrated RAG Service.
    Integrates retrieval, reranking, knowledge graph contexts, LLM synthesis, and citation generation.
    """

    @abstractmethod
    def generate_answer(self, query: str, user_permissions: List[str]) -> Dict[str, Any]:
        """
        Processes a user query by executing the entire RAG pipeline:
        1. Retrieval (BM25 + Vector + Permissions filter)
        2. Graph Expansion
        3. Reranking
        4. Context Assembly
        5. LLM Synthesis
        6. Citations generation
        """
        pass
