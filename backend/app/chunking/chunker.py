import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ChunkPayload(BaseModel):
    """Pydantic model representing a text chunk with positional metadata."""
    chunk_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    chunk_number: int
    text: str
    start_offset: int
    end_offset: int
    character_count: int


class BaseChunker(ABC):
    """Base interface for all chunking algorithms (semantic-ready)."""

    @abstractmethod
    def chunk_text(self, text: str) -> List[ChunkPayload]:
        """Split input text into chunks.

        Args:
            text: Raw document string content.

        Returns:
            List of ChunkPayload structures.
        """
        pass


class RecursiveCharacterChunker(BaseChunker):
    """Splits text recursively using a list of separators to keep paragraphs and sentences intact."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] | None = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Hierarchical separators descending from paragraph -> sentence -> word -> character
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """Recursive split helper."""
        if len(text) <= self.chunk_size:
            return [text]

        # Find the appropriate separator
        separator = separators[0] if separators else ""
        for s in separators:
            if s == "":
                separator = s
                break
            if s in text:
                separator = s
                break

        # Split text by separator
        if separator != "":
            splits = text.split(separator)
        else:
            # If no separators left, split by character
            splits = list(text)

        # Re-merge splits that are too small or recursively split those that are too large
        result_splits = []
        for split in splits:
            if len(split) > self.chunk_size:
                # Recursively split large segments using remaining separators
                next_seps = separators[separators.index(separator) + 1 :] if separator in separators else []
                result_splits.extend(self._split_text(split, next_seps))
            else:
                result_splits.append(split)

        return result_splits

    def chunk_text(self, text: str) -> List[ChunkPayload]:
        """Run recursive chunking and compute character offsets."""
        if not text.strip():
            return []

        # Step 1: Split text into small fragments
        fragments = self._split_text(text, self.separators)

        # Step 2: Merge fragments into chunks with overlap
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_length = 0

        for fragment in fragments:
            # If fragment itself is empty, ignore
            if not fragment:
                continue
            
            # If adding this fragment exceeds chunk size, save current chunk and start a new one
            if current_length + len(fragment) > self.chunk_size:
                if current_chunk:
                    chunks.append("".join(current_chunk))
                
                # Setup overlap for next chunk: merge backward from current list
                overlap_chunk = []
                overlap_len = 0
                for f in reversed(current_chunk):
                    if overlap_len + len(f) <= self.chunk_overlap:
                        overlap_chunk.insert(0, f)
                        overlap_len += len(f)
                    else:
                        break
                current_chunk = overlap_chunk
                current_length = overlap_len

            current_chunk.append(fragment)
            current_length += len(fragment)

        if current_chunk:
            chunks.append("".join(current_chunk))

        # Step 3: Map chunks to payload objects calculating absolute offsets
        payloads: List[ChunkPayload] = []
        last_search_index = 0

        for idx, chunk_text in enumerate(chunks):
            # Locate position of this chunk inside the original text
            start_offset = text.find(chunk_text, last_search_index)
            if start_offset == -1:
                # Fallback to general search if search index is somehow offset
                start_offset = text.find(chunk_text)
            
            if start_offset != -1:
                end_offset = start_offset + len(chunk_text)
                last_search_index = start_offset + max(1, self.chunk_overlap)
            else:
                start_offset = 0
                end_offset = 0

            payloads.append(
                ChunkPayload(
                    chunk_number=idx + 1,
                    text=chunk_text,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    character_count=len(chunk_text),
                )
            )

        return payloads
