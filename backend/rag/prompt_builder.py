from .models import AssembledContext, RagPrompt

class PromptBuilder:
    """
    Renders structured instructions containing assembled context blocks for LLM APIs.
    """

    def construct(self, context: AssembledContext, query: str) -> RagPrompt:
        # Format retrieved documents text
        docs_section = []
        for i, chunk in enumerate(context.retrieved_chunks):
            payload = chunk.get("payload") or chunk
            doc_id = payload.get("document_id") or chunk.get("id") or "Unknown"
            
            # Retrieve source metadata details if available
            metadata_info = payload.get("metadata", {})
            permissions = metadata_info.get("permissions", [])
            
            docs_section.append(
                f"Document [{i+1}]: {doc_id}\n"
                f"Permissions: {', '.join(permissions)}\n"
                f"Source Info: {metadata_info}"
            )
        docs_text = "\n\n".join(docs_section) if docs_section else "No documents retrieved."

        # Format expanded graph context
        graph_context = context.graph_context
        entities_text = "\n".join([f"  - [{e['label']}] {e['node_id']} | Properties: {e['properties']}" for e in graph_context.entities])
        relationships_text = "\n".join([f"  - ({r['source_id']}) -[{r['type']}]-> ({r['target_id']})" for r in graph_context.relationships])
        
        graph_text = f"Entities:\n{entities_text}\n\nRelationships:\n{relationships_text}"

        system_instruction = (
            "You are a helpful AI assistant. Answer the user's question ONLY using the provided retrieved documents "
            "and knowledge graph context. Explain your reasoning step-by-step and provide supporting evidence "
            "from the context (documents or graph relations)."
        )

        user_prompt = (
            f"User Question:\n{query}\n\n"
            f"--- Retrieved Documents ---\n"
            f"{docs_text}\n\n"
            f"--- Knowledge Graph Context ---\n"
            f"{graph_text}\n\n"
            f"--- Instructions ---\n"
            f"1. Answer the question ONLY using the provided context.\n"
            f"2. Explain your reasoning step-by-step.\n"
            f"3. Provide supporting evidence from the context (e.g. document IDs or graph relationships)."
        )

        return RagPrompt(
            system_instruction=system_instruction,
            user_prompt=user_prompt
        )
