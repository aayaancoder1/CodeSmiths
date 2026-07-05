from typing import Dict
from .models import LatencyMetrics

class LatencyTracker:
    """
    Measures time parameters for pipeline processing stages.
    """

    def process(self, timings: Dict[str, float]) -> LatencyMetrics:
        # Placeholder metrics conversion
        return LatencyMetrics(
            retrieval_ms=timings.get("retrieval", 0.0),
            graph_ms=timings.get("graph", 0.0),
            total_ms=timings.get("total", 0.0)
        )
