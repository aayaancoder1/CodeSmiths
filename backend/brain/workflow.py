from typing import Dict, Any

class BrainWorkflow:
    """
    Manages transaction state checkpoints and logs across pipeline runs.
    """

    def __init__(self):
        self._execution_history: Dict[str, Any] = {}

    def log_state(self, pipeline_id: str, stage: str, state: Dict[str, Any]) -> None:
        """Register transactional outputs or milestones for auditing."""
        if pipeline_id not in self._execution_history:
            self._execution_history[pipeline_id] = {}
        self._execution_history[pipeline_id][stage] = state
