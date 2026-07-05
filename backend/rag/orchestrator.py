from typing import List, Dict, Any
from .models import RagRequest, RagResponse, AssembledContext, ExpandedGraphContext
from .graph_expander import GraphContextExpander
from .context_builder import ContextBuilder
from .prompt_builder import PromptBuilder
from .synthesis import SynthesisService

class RagOrchestrator:
    """
    Coordinates retrieval queries, graph expansions, context assemblies,
    prompt bindings, and LLM text synthesis steps.
    """

    def __init__(
        self,
        expander: GraphContextExpander,
        builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        synthesis: SynthesisService
    ):
        self.expander = expander
        self.builder = builder
        self.prompt_builder = prompt_builder
        self.synthesis = synthesis

    def execute_pipeline(self, request: RagRequest, retrieved_chunks: List[Dict[str, Any]], seed_nodes: List[Dict[str, Any]]) -> RagResponse:
        # Step 1: Expand neighborhood graph context
        graph_context = self.expander.expand_graph(retrieved_chunks, request.tenant_id)
        
        # Step 2: Combine texts and graph nodes into unified context blocks
        context = self.builder.build(retrieved_chunks, graph_context)
        
        # Step 3: Format the context elements into prompts
        prompt = self.prompt_builder.construct(context, request.query)
        
        # Step 4: Synthesize final answer via LLM call
        answer = self.synthesis.synthesize(prompt)
        
        return RagResponse(
            answer=answer,
            context=context
        )
