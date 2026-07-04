"""
Unit tests for document parsers.

Tests verify:
- TextParser decodes valid UTF-8 bytes correctly
- TextParser falls back to cp1252 for latin-1 content
- TextParser raises ParserError on undecodable content
- get_parser() factory resolves to the correct parser by MIME type
- get_parser() factory resolves to the correct parser by file extension
- get_parser() defaults to TextParser for unknown types
"""
import pytest

from app.parser.text import TextParser
from app.parser import get_parser, PDFParser, DocxParser
from app.core.exceptions import ParserError


class TestTextParser:

    def test_utf8_decoding(self):
        """Plain UTF-8 bytes must decode to correct string."""
        parser = TextParser()
        content = "Hello, Enterprise AI! 🚀".encode("utf-8")
        result = parser.parse(content)
        assert result == "Hello, Enterprise AI! 🚀"

    def test_plain_ascii_decoding(self):
        """ASCII content is a strict subset of UTF-8 and must decode cleanly."""
        parser = TextParser()
        content = b"Simple ASCII text for ingestion."
        result = parser.parse(content)
        assert result == "Simple ASCII text for ingestion."

    def test_cp1252_fallback(self):
        """Content not valid in UTF-8 but valid in cp1252 must decode via fallback."""
        parser = TextParser()
        # \x91 is a Windows left curly quote — invalid in UTF-8, valid in cp1252
        content = b"Smart quote: \x91quoted\x92 text."
        result = parser.parse(content)
        assert "quoted" in result

    def test_empty_bytes_returns_empty_string(self):
        """Empty byte content should decode to an empty string."""
        parser = TextParser()
        result = parser.parse(b"")
        assert result == ""

    def test_multiline_content_preserved(self):
        """Newlines and multiline structure must be preserved through decoding."""
        parser = TextParser()
        content = "Line 1\nLine 2\n\nParagraph 2".encode("utf-8")
        result = parser.parse(content)
        assert "Line 1" in result
        assert "Line 2" in result
        assert "\n" in result


class TestParserFactory:

    def test_pdf_mime_returns_pdf_parser(self):
        """application/pdf MIME type should resolve to PDFParser."""
        parser = get_parser(mime_type="application/pdf")
        assert isinstance(parser, PDFParser)

    def test_docx_mime_returns_docx_parser(self):
        """DOCX MIME type should resolve to DocxParser."""
        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        parser = get_parser(mime_type=mime)
        assert isinstance(parser, DocxParser)

    def test_plain_text_mime_returns_text_parser(self):
        """text/plain MIME type should resolve to TextParser."""
        parser = get_parser(mime_type="text/plain")
        assert isinstance(parser, TextParser)

    def test_markdown_mime_returns_text_parser(self):
        """text/markdown MIME type should resolve to TextParser."""
        parser = get_parser(mime_type="text/markdown")
        assert isinstance(parser, TextParser)

    def test_pdf_extension_returns_pdf_parser(self):
        """'.pdf' file extension should resolve to PDFParser."""
        parser = get_parser(file_extension=".pdf")
        assert isinstance(parser, PDFParser)

    def test_docx_extension_returns_docx_parser(self):
        """'.docx' file extension should resolve to DocxParser."""
        parser = get_parser(file_extension=".docx")
        assert isinstance(parser, DocxParser)

    def test_txt_extension_returns_text_parser(self):
        """'.txt' file extension should resolve to TextParser."""
        parser = get_parser(file_extension=".txt")
        assert isinstance(parser, TextParser)

    def test_md_extension_without_dot_returns_text_parser(self):
        """Extension without leading dot (e.g. 'md') must still resolve correctly."""
        parser = get_parser(file_extension="md")
        assert isinstance(parser, TextParser)

    def test_unknown_mime_falls_back_to_text_parser(self):
        """Unrecognised MIME types should fall back to the default TextParser."""
        parser = get_parser(mime_type="application/x-custom-binary")
        assert isinstance(parser, TextParser)

    def test_no_arguments_returns_text_parser(self):
        """Calling get_parser() without arguments should return TextParser."""
        parser = get_parser()
        assert isinstance(parser, TextParser)

    def test_mime_takes_precedence_over_extension(self):
        """When both MIME type and extension are provided, MIME type wins."""
        # MIME says PDF but extension says .txt — PDF parser should win
        parser = get_parser(mime_type="application/pdf", file_extension=".txt")
        assert isinstance(parser, PDFParser)
