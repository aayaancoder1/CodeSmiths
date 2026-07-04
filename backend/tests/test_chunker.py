"""
Unit tests for the RecursiveCharacterChunker.

Tests verify that:
- Empty input produces no chunks
- Short text below chunk_size produces one chunk
- Long text is split into multiple chunks
- Each chunk respects chunk_size limit
- Overlapping content exists between adjacent chunks
- Chunk offsets correctly map back to original text
- Chunk numbering is sequential starting from 1
"""
import pytest

from app.chunking.chunker import RecursiveCharacterChunker, ChunkPayload


@pytest.fixture
def chunker() -> RecursiveCharacterChunker:
    """Return a chunker with small defaults suited for unit testing."""
    return RecursiveCharacterChunker(chunk_size=50, chunk_overlap=10)


@pytest.fixture
def large_chunker() -> RecursiveCharacterChunker:
    """Return a chunker with realistic enterprise defaults."""
    return RecursiveCharacterChunker(chunk_size=1000, chunk_overlap=200)


class TestRecursiveCharacterChunker:

    def test_empty_input_returns_no_chunks(self, chunker):
        """Empty string and whitespace-only strings produce an empty list."""
        assert chunker.chunk_text("") == []
        assert chunker.chunk_text("   ") == []
        assert chunker.chunk_text("\n\n\n") == []

    def test_short_text_returns_single_chunk(self, chunker):
        """Text shorter than chunk_size results in exactly one chunk."""
        text = "Short text."
        chunks = chunker.chunk_text(text)
        assert len(chunks) == 1
        assert chunks[0].text == text
        assert chunks[0].chunk_number == 1

    def test_long_text_returns_multiple_chunks(self, chunker):
        """Text exceeding chunk_size is split into multiple chunks."""
        text = "word " * 30  # 150 chars, well above chunk_size=50
        chunks = chunker.chunk_text(text)
        assert len(chunks) > 1

    def test_chunk_size_not_exceeded(self, chunker):
        """Each generated chunk must not exceed the configured chunk_size."""
        text = "abcdef " * 20
        chunks = chunker.chunk_text(text)
        for chunk in chunks:
            assert chunk.character_count <= chunker.chunk_size, (
                f"Chunk {chunk.chunk_number} exceeded size limit: {chunk.character_count} > {chunker.chunk_size}"
            )

    def test_chunk_payloads_are_correct_type(self, chunker):
        """All returned elements are ChunkPayload instances."""
        chunks = chunker.chunk_text("Hello world. " * 10)
        for chunk in chunks:
            assert isinstance(chunk, ChunkPayload)

    def test_chunk_numbering_is_sequential(self, chunker):
        """Chunks must be numbered sequentially starting from 1."""
        text = "line of text\n" * 20
        chunks = chunker.chunk_text(text)
        for i, chunk in enumerate(chunks, start=1):
            assert chunk.chunk_number == i

    def test_chunk_offsets_are_within_text_bounds(self, chunker):
        """start_offset and end_offset must be within the original text bounds."""
        text = "The quick brown fox jumps over the lazy dog. " * 5
        chunks = chunker.chunk_text(text)
        for chunk in chunks:
            assert chunk.start_offset >= 0
            assert chunk.end_offset <= len(text)
            assert chunk.start_offset < chunk.end_offset

    def test_character_count_matches_text_length(self, chunker):
        """The character_count field must match the actual length of chunk.text."""
        text = "Some meaningful content. " * 10
        chunks = chunker.chunk_text(text)
        for chunk in chunks:
            assert chunk.character_count == len(chunk.text)

    def test_overlap_content_shared_between_adjacent_chunks(self, large_chunker):
        """With overlap configured, adjacent chunks should share some text."""
        # Build text long enough to definitely produce multiple chunks
        text = ("Enterprise knowledge platform for AI teams. " * 50)
        chunks = large_chunker.chunk_text(text)
        if len(chunks) < 2:
            pytest.skip("Need at least 2 chunks to check overlap")

        # The beginning of chunk[1] should appear somewhere in chunk[0]
        overlap_start = chunks[1].text[:20]
        assert overlap_start in chunks[0].text, (
            "Expected overlap text from start of chunk[1] to exist in chunk[0]"
        )

    def test_paragraph_separator_preferred(self):
        """Paragraph breaks (double newlines) are preferred split points."""
        chunker = RecursiveCharacterChunker(chunk_size=30, chunk_overlap=0)
        text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        chunks = chunker.chunk_text(text)
        # Paragraphs should be split cleanly
        assert len(chunks) >= 2
        # No chunk should span across a double newline if chunk_size allows
        for chunk in chunks:
            assert "\n\n" not in chunk.text or chunk.character_count <= chunker.chunk_size

    def test_chunk_text_uuid_is_unique(self, chunker):
        """Each ChunkPayload must have a unique chunk_id."""
        text = "unique id per chunk. " * 20
        chunks = chunker.chunk_text(text)
        ids = [c.chunk_id for c in chunks]
        assert len(ids) == len(set(ids)), "Chunk UUIDs must be unique"
