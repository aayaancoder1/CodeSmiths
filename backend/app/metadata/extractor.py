import re
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.connectors.base import ConnectorDocument


class MetadataPayload(BaseModel):
    """Pydantic model representing extracted document metadata."""
    title: str
    author: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    file_type: str
    source: str
    word_count: int
    language: str = "en"
    tags: List[str] = Field(default_factory=list)
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseMetadataExtractor(BaseModel):
    """Abstract interface for document metadata extraction."""

    def extract(self, doc: ConnectorDocument, parsed_text: str) -> MetadataPayload:
        """Extract metadata attributes from raw text and connector payloads."""
        pass


class StandardMetadataExtractor(BaseMetadataExtractor):
    """Standard metadata extraction service running heuristics on extracted text."""

    def _infer_title(self, doc_title: str, text: str) -> str:
        """Infers a document title by falling back to the first non-empty header or line."""
        if doc_title and doc_title.strip():
            return doc_title.strip()

        # Check for first line markdown header (e.g., # Title)
        header_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if header_match:
            return header_match.group(1).strip()

        # Fall back to first non-empty line
        for line in text.split("\n"):
            if line.strip():
                # Cap title length
                return line.strip()[:100]

        return "Untitled Document"

    def _generate_tags(self, text: str) -> List[str]:
        """Runs simple keyword search to generate tags from document contents."""
        keywords = {
            "strategy": ["strategy", "planning", "roadmap", "goals"],
            "financial": ["finance", "budget", "revenue", "costs", "profit"],
            "engineering": ["engineering", "architecture", "code", "database", "api"],
            "operations": ["operation", "sop", "process", "workflow", "safety"],
            "marketing": ["marketing", "campaign", "social media", "sales"],
            "onboarding": ["onboarding", "welcome", "employee", "training"],
        }
        
        tags = []
        text_lower = text.lower()
        for tag, synonyms in keywords.items():
            for syn in synonyms:
                if syn in text_lower:
                    tags.append(tag)
                    break
        return tags

    def extract(self, doc: ConnectorDocument, parsed_text: str) -> MetadataPayload:
        """Perform metadata extraction from raw text and source payloads."""
        # Calculate word count
        words = parsed_text.split()
        word_count = len(words)

        # Infer title
        title = self._infer_title(doc.title, parsed_text)

        # Generate tags
        tags = self._generate_tags(parsed_text)

        return MetadataPayload(
            title=title,
            author=doc.author or "System Ingestion",
            created_at=doc.created_at or datetime.now(),
            updated_at=doc.updated_at or datetime.now(),
            file_type=doc.mime_type,
            source=doc.metadata.get("connector_type") or "manual",
            word_count=word_count,
            language="en",  # Placeholder
            tags=tags,
            custom_metadata=doc.metadata,
        )
