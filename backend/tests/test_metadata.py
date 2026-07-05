"""
Unit tests for StandardMetadataExtractor.

Tests verify:
- Word count is computed correctly
- Title is taken from ConnectorDocument when provided
- Title falls back to markdown header in text
- Title falls back to first non-empty line
- Title fallback for blank text is 'Untitled Document'
- Tags are inferred correctly from keyword presence
- Tags do not duplicate when multiple synonyms of same tag match
- Custom metadata from ConnectorDocument is carried through
"""
import pytest
from datetime import datetime

from app.metadata.extractor import StandardMetadataExtractor, MetadataPayload
from app.connectors.base import ConnectorDocument


def make_doc(
    title: str = "Test Doc",
    author: str | None = None,
    mime_type: str = "text/plain",
    file_extension: str = ".txt",
    metadata: dict | None = None,
) -> ConnectorDocument:
    """Helper factory for ConnectorDocument test instances."""
    return ConnectorDocument(
        source_id="test-001",
        title=title,
        content=b"placeholder",
        mime_type=mime_type,
        file_extension=file_extension,
        author=author,
        metadata=metadata or {},
    )


@pytest.fixture
def extractor() -> StandardMetadataExtractor:
    return StandardMetadataExtractor()


class TestStandardMetadataExtractor:

    def test_word_count_is_correct(self, extractor):
        """word_count must equal the number of whitespace-delimited tokens."""
        doc = make_doc()
        text = "alpha beta gamma delta epsilon"
        result = extractor.extract(doc, text)
        assert result.word_count == 5

    def test_word_count_multiline(self, extractor):
        """word_count must count across multiple lines."""
        doc = make_doc()
        text = "word1 word2\nword3 word4\nword5"
        result = extractor.extract(doc, text)
        assert result.word_count == 5

    def test_title_taken_from_doc_when_provided(self, extractor):
        """Title should come from ConnectorDocument.title when non-empty."""
        doc = make_doc(title="My Official Report")
        result = extractor.extract(doc, "Some text here.")
        assert result.title == "My Official Report"

    def test_title_fallback_to_markdown_header(self, extractor):
        """When doc.title is empty, title should be extracted from first '# Header' line."""
        doc = make_doc(title="")
        text = "# Strategic Planning Document\n\nContent follows."
        result = extractor.extract(doc, text)
        assert result.title == "Strategic Planning Document"

    def test_title_fallback_to_first_line(self, extractor):
        """When doc.title is empty and no markdown header, first non-empty line is used."""
        doc = make_doc(title="")
        text = "First Line Title\n\nBody of document."
        result = extractor.extract(doc, text)
        assert result.title == "First Line Title"

    def test_title_fallback_for_empty_text(self, extractor):
        """When doc.title and text are both empty, title defaults to 'Untitled Document'."""
        doc = make_doc(title="")
        result = extractor.extract(doc, "")
        assert result.title == "Untitled Document"

    def test_author_from_doc(self, extractor):
        """Author should be taken from ConnectorDocument.author when provided."""
        doc = make_doc(author="Jane Smith")
        result = extractor.extract(doc, "Document content.")
        assert result.author == "Jane Smith"

    def test_author_default_when_none(self, extractor):
        """When ConnectorDocument.author is None, author defaults to 'System Ingestion'."""
        doc = make_doc(author=None)
        result = extractor.extract(doc, "Document content.")
        assert result.author == "System Ingestion"

    def test_file_type_matches_mime(self, extractor):
        """file_type in MetadataPayload must match the connector doc's mime_type."""
        doc = make_doc(mime_type="application/pdf")
        result = extractor.extract(doc, "PDF document text.")
        assert result.file_type == "application/pdf"

    def test_tag_engineering_inferred(self, extractor):
        """Text containing engineering keywords must produce the 'engineering' tag."""
        doc = make_doc()
        text = "We need to review the database architecture and API contracts."
        result = extractor.extract(doc, text)
        assert "engineering" in result.tags

    def test_tag_financial_inferred(self, extractor):
        """Text containing financial keywords must produce the 'financial' tag."""
        doc = make_doc()
        text = "Q3 budget review shows revenue growth and stable profit margins."
        result = extractor.extract(doc, text)
        assert "financial" in result.tags

    def test_tags_do_not_duplicate(self, extractor):
        """Each tag must appear at most once even when multiple synonyms match."""
        doc = make_doc()
        # Both 'engineering' and 'architecture' are synonyms for the 'engineering' tag
        text = "The engineering team built an architecture for the code database."
        result = extractor.extract(doc, text)
        assert result.tags.count("engineering") == 1

    def test_no_tags_for_irrelevant_text(self, extractor):
        """Text with no keyword matches should produce an empty tags list."""
        doc = make_doc()
        text = "Lorem ipsum dolor sit amet consectetur adipiscing elit."
        result = extractor.extract(doc, text)
        assert result.tags == []

    def test_custom_metadata_passed_through(self, extractor):
        """Custom metadata dict from ConnectorDocument should be preserved verbatim."""
        custom = {"connector_type": "google_drive", "file_id": "abc123"}
        doc = make_doc(metadata=custom)
        result = extractor.extract(doc, "Some content.")
        assert result.custom_metadata == custom

    def test_result_is_metadata_payload(self, extractor):
        """extract() must always return a MetadataPayload instance."""
        doc = make_doc()
        result = extractor.extract(doc, "Content here.")
        assert isinstance(result, MetadataPayload)
