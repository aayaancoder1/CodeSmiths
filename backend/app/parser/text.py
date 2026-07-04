import logging
from app.parser.base import BaseParser
from app.core.exceptions import ParserError

logger = logging.getLogger(__name__)


class TextParser(BaseParser):
    """Parser for raw TXT and Markdown files."""

    def parse(self, content: bytes) -> str:
        """Decode raw bytes into a clean string, falling back to alternative encodings if necessary."""
        try:
            # First try UTF-8 decoding (standard)
            return content.decode("utf-8")
        except UnicodeDecodeError as e:
            logger.warning("TextParser: UTF-8 decoding failed, falling back to cp1252/latin-1.")
            try:
                return content.decode("cp1252")
            except Exception as ex:
                raise ParserError("TXT/Markdown", "Failed to decode file contents.", {"original_error": str(ex)})
