from abc import ABC, abstractmethod
from typing import Dict, Any

class ToolAdapter(ABC):
    """
    Common interface that all tool adapters must implement.
    """

    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the tool with the provided inputs.
        """
        pass

    @abstractmethod
    def validate_input(self, inputs: Dict[str, Any]) -> bool:
        """
        Validates the structure and presence of required inputs for the tool.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns metadata about the tool (e.g. description, input requirements).
        """
        pass
