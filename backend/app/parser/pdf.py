import io
import logging
from pypdf import PdfReader
from app.parser.base import BaseParser
from app.core.exceptions import ParserError

logger = logging.getLogger(__name__)


class PDFParser(BaseParser):
    """Parser extracting plain text from PDF files using pypdf."""

    def parse(self, content: bytes) -> str:
        try:
            # Wrap content bytes in a BytesIO stream
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            
            text_pages = []
            for page_num, page in enumerate(reader.pages):
                try:
                    text = page.extract_text()
                    if text:
                        text_pages.append(text)
                except Exception as page_err:
                    logger.warning(f"PDFParser: Skipping page {page_num} due to extraction failure: {page_err}")
            
            return "\n\n".join(text_pages)
        except Exception as e:
            raise ParserError("PDF", "Failed to extract text from PDF document.", {"original_error": str(e)})
