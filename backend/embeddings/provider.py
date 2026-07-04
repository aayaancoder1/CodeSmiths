from abc import ABC, abstractmethod
from typing import List

class IEmbeddingProvider(ABC):
    """
    Interface for the Embedding Provider abstraction (e.g. Local SentenceTransformers, OpenAI, Cohere).
    """

    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """Returns the dimensionality of the generated vectors."""
        pass

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generates embedding vectors for the given texts."""
        pass
