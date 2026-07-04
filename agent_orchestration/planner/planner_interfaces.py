from abc import ABC, abstractmethod
from typing import Dict, Any

class IPlannerAgent(ABC):
    """
    Interface for the Planner Agent.
    """

    @abstractmethod
    def create_plan(self, request: str) -> Any:
        """
        Creates an execution plan from a user request.
        """
        pass

    @abstractmethod
    def validate_plan(self, plan: Any) -> bool:
        """
        Validates the structure and soundness of the generated execution plan.
        """
        pass

    @abstractmethod
    def build_task_graph(self, plan: Any) -> Dict[str, Any]:
        """
        Builds an ordered task graph from the execution plan.
        """
        pass
