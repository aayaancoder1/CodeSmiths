from typing import List, Any
from .interface import IHybridRetrievalService
from .models import HybridSearchInput, HybridSearchOutput, FusedResult
from .fusion import IFusionStrategy, ReciprocalRankFusion
from .aggregator import Aggregator
from .ranker import HybridRanker

class HybridRetrievalService(IHybridRetrievalService):
    """
    Placeholder service implementation managing RRF blending, aggregation, and reranking routing.
    """

    def __init__(self, fusion_strategy: IFusionStrategy, aggregator: Aggregator, ranker: HybridRanker):
        self.fusion_strategy = fusion_strategy
        self.aggregator = aggregator
        self.ranker = ranker

    def hybrid_search(self, inputs: HybridSearchInput) -> HybridSearchOutput:
        fused = self.reciprocal_rank_fusion(inputs.vector_results, inputs.bm25_results)
        reranked = self.rerank_results(fused, inputs.query)
        return HybridSearchOutput(merged_results=reranked[:inputs.top_k])

    def reciprocal_rank_fusion(self, vector_results: List[Any], bm25_results: List[Any], k: int = 60) -> List[FusedResult]:
        # Using configured fusion strategy (e.g. RRF)
        return self.fusion_strategy.fuse(vector_results, bm25_results)

    def aggregate_results(self, vector_results: List[Any], bm25_results: List[Any]) -> List[FusedResult]:
        return self.aggregator.aggregate(vector_results, bm25_results)

    def rerank_results(self, results: List[FusedResult], query: str) -> List[FusedResult]:
        return self.ranker.rerank(query, results)
