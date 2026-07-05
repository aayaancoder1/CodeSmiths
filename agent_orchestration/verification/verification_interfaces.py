from abc import ABC, abstractmethod
from typing import Any

class VerificationRule(ABC):
    """
    Interface for rule-based deterministic validation checks.
    """

    @abstractmethod
    def validate(self, result: Any) -> bool:
        """
        Executes the validation rule against the execution result.
        Returns True if validation passes, otherwise raises validation exception.
        """
        pass

    @abstractmethod
    def get_rule_name(self) -> str:
        """
        Returns the unique identifier/name for this validation rule.
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Returns a short description of what this rule validates.
        """
        pass
