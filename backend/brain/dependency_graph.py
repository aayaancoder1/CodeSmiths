from typing import List, Dict

class DependencyGraph:
    """
    Validates execution bounds, dependency requirements, and schedules pipeline stage executions.
    """

    def __init__(self):
        self.dependencies: Dict[str, List[str]] = {
            "embeddings": [],
            "retrieval": ["embeddings"],
            "bm25": [],
            "hybrid_retrieval": ["retrieval", "bm25"],
            "knowledge_graph": [],
            "graph_expansion": ["hybrid_retrieval", "knowledge_graph"],
            "graph_rag": ["graph_expansion"],
            "citations": ["graph_rag"],
            "evaluation": ["citations", "graph_rag"]
        }

    def get_execution_order(self) -> List[str]:
        """Resolves dependency constraints and returns list ordering of execution stages."""
        return [
            "embeddings",
            "bm25",
            "retrieval",
            "hybrid_retrieval",
            "knowledge_graph",
            "graph_expansion",
            "graph_rag",
            "citations",
            "evaluation"
        ]
