from .models import AssembledContext, RagPrompt

class PromptBuilder:
    """
    Renders structured instructions containing assembled context blocks for LLM APIs.
    """

    def construct(self, context: AssembledContext, query: str) -> RagPrompt:
        # Placeholder prompt formatting
        return RagPrompt(
            system_instruction="Analyze context and relations to synthesize a factual answer.",
            user_prompt=f"Context: {context}\nQuery: {query}"
        )
