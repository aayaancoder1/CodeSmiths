from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract Base Class for all document content parsers."""

    @abstractmethod
    def parse(self, content: bytes) -> str:
        """Extract plain text from document binary contents.

        Args:
            content: Raw document file content bytes.

        Returns:
            Cleaned plain text representation of the document.
        """
        pass
