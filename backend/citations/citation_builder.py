from typing import List
from .models import Citation, SourceReference

class CitationBuilder:
    """
    Constructs citations mapping specific character spans of syntheses
    back to matched references.
    """

    def build(self, answer: str, references: List[SourceReference]) -> List[Citation]:
        doc_refs = [ref for ref in references if ref.type == "document"]
        citations = []
        
        for idx, ref in enumerate(doc_refs):
            # Check if source_id is explicitly mentioned in the text
            doc_name = ref.source_id
            start_idx = answer.find(doc_name)
            if start_idx != -1:
                citations.append(Citation(
                    citation_id=f"cit_{idx+1}",
                    text_span=[start_idx, start_idx + len(doc_name)],
                    sources=[ref],
                    confidence_score=ref.metadata.get("score", 0.9)
                ))
            else:
                # Default citation covering the entire text block
                citations.append(Citation(
                    citation_id=f"cit_{idx+1}",
                    text_span=[0, len(answer)],
                    sources=[ref],
                    confidence_score=ref.metadata.get("score", 0.9)
                ))
        return citations
