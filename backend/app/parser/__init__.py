from typing import Dict, Type
from app.parser.base import BaseParser
from app.parser.pdf import PDFParser
from app.parser.docx import DocxParser
from app.parser.text import TextParser

# Map MIME types to corresponding parser classes
PARSER_MIME_REGISTRY: Dict[str, Type[BaseParser]] = {
    "application/pdf": PDFParser,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocxParser,
    "text/plain": TextParser,
    "text/markdown": TextParser,
}

# Map file extensions to corresponding parser classes (fallback option)
PARSER_EXT_REGISTRY: Dict[str, Type[BaseParser]] = {
    ".pdf": PDFParser,
    ".docx": DocxParser,
    ".txt": TextParser,
    ".md": TextParser,
    ".markdown": TextParser,
}


def get_parser(mime_type: str | None = None, file_extension: str | None = None) -> BaseParser:
    """Factory function resolving and returning the appropriate parser instance.

    Defaults to TextParser if no specific match is found.
    """
    if mime_type and mime_type.lower() in PARSER_MIME_REGISTRY:
        return PARSER_MIME_REGISTRY[mime_type.lower()]()

    if file_extension:
        ext = file_extension.lower()
        if not ext.startswith("."):
            ext = f".{ext}"
        if ext in PARSER_EXT_REGISTRY:
            return PARSER_EXT_REGISTRY[ext]()

    # Fallback to TextParser which reads bytes as generic string
    return TextParser()


__all__ = [
    "BaseParser",
    "PDFParser",
    "DocxParser",
    "TextParser",
    "get_parser",
]
