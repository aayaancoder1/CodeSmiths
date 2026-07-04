from typing import List
from .models import Citation, SourceReference

class CitationBuilder:
    """
    Constructs citations mapping specific character spans of syntheses
    back to matched references.
    """

    def build(self, answer: str, references: List[SourceReference]) -> List[Citation]:
        # Placeholder citation builder returning default covers
        return [
            Citation(
                citation_id="cit_1",
                text_span=[0, len(answer)],
                sources=references,
                confidence_score=0.95
            )
        ]
