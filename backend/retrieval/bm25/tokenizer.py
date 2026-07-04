from abc import ABC, abstractmethod
from typing import List

class ITokenizer(ABC):
    """
    Interface for lexical query and document tokenization.
    """

    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        """Convert a string into a list of normalized tokens/stems."""
        pass

class SimpleTokenizer(ITokenizer):
    """
    Simple mock tokenizer split on whitespace and alphanumeric sequences.
    """
    def tokenize(self, text: str) -> List[str]:
        # Placeholder lowercase splitting logic
        return [t.strip().lower() for t in text.split() if t.strip()]
