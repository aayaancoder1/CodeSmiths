from typing import List, Any
from .models import FusedResult

class Aggregator:
    """
    Collects, deduplicates, and resolves metadata overlays for overlapping chunks
    retrieved from multiple database subsystems.
    """

    def aggregate(self, vector_results: List[Any], bm25_results: List[Any]) -> List[FusedResult]:
        # Placeholder aggregation logic returning deduplicated items
        return [
            FusedResult(
                chunk_id="agg_chunk_1",
                document_id="doc_1",
                text="Aggregated search results",
                fusion_score=1.0,
                metadata={}
            )
        ]
