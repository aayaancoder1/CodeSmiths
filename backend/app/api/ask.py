"""
GraphRAG API endpoint — POST /api/ask

Wires the existing verified GraphRAG pipeline (Qdrant → Neo4j → Gemini → Citations)
into FastAPI. Uses the exact same initialization pattern as test_citations.py.
"""
import os
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["GraphRAG"])


# --- Request / Response Schemas ---

class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="The user's question")
    tenant_id: str = Field(default="tenant-123", description="Tenant isolation ID")


class SourceItem(BaseModel):
    index: int
    document_id: str


class EntityItem(BaseModel):
    label: str
    node_id: str
    properties: dict = {}


class RelationshipItem(BaseModel):
    source_id: str
    target_id: str
    type: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceItem] = []
    entities: list[EntityItem] = []
    relationships: list[RelationshipItem] = []


# --- Lazy-initialized singletons ---
# Heavy ML models and DB connections are initialized once on first request,
# not at import time, so the server starts fast.

_initialized = False
_embedding_service = None
_qdrant_client = None
_neo4j_adapter = None
_rag_service = None
_citation_service = None


def _ensure_initialized():
    """Initialize all subsystem connections on first call. Thread-safe via GIL for demo."""
    global _initialized, _embedding_service, _qdrant_client, _neo4j_adapter, _rag_service, _citation_service

    if _initialized:
        return

    logger.info("Initializing GraphRAG pipeline subsystems...")

    # 1. Embeddings
    from backend.embeddings.provider import SentenceTransformerProvider
    from backend.embeddings.service import EmbeddingService
    from backend.embeddings.qdrant_client import QdrantClientAdapter

    provider = SentenceTransformerProvider()
    _qdrant_client = QdrantClientAdapter(url="http://localhost:6333")
    _embedding_service = EmbeddingService(provider=provider, qdrant_client=_qdrant_client)

    # 2. Neo4j
    from backend.graph.neo4j_adapter import Neo4jAdapter

    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password123")
    _neo4j_adapter = Neo4jAdapter(uri=uri, user=user, password=password)
    _neo4j_adapter.connect()

    # 3. RAG orchestrator (same wiring as test_graph_rag.py)
    from backend.rag.graph_expander import GraphContextExpander
    from backend.rag.context_builder import ContextBuilder
    from backend.rag.prompt_builder import PromptBuilder
    from backend.rag.synthesis import SynthesisService
    from backend.rag.orchestrator import RagOrchestrator
    from backend.rag.service import RagService

    expander = GraphContextExpander(neo4j_adapter=_neo4j_adapter)
    builder = ContextBuilder()
    prompt_builder = PromptBuilder()
    synthesis = SynthesisService()

    orchestrator = RagOrchestrator(
        expander=expander,
        builder=builder,
        prompt_builder=prompt_builder,
        synthesis=synthesis
    )
    _rag_service = RagService(orchestrator=orchestrator)

    # 4. Citations
    from backend.citations.source_tracker import SourceTracker
    from backend.citations.citation_builder import CitationBuilder
    from backend.citations.provenance import ProvenanceMapper
    from backend.citations.service import CitationService

    tracker = SourceTracker()
    cit_builder = CitationBuilder()
    mapper = ProvenanceMapper()
    _citation_service = CitationService(tracker=tracker, builder=cit_builder, mapper=mapper)

    _initialized = True
    logger.info("GraphRAG pipeline initialized successfully.")


# --- Endpoint ---

@router.post("/ask", response_model=AskResponse, summary="Ask the GraphRAG pipeline a question")
async def ask(request: AskRequest):
    """
    End-to-end GraphRAG query:
    1. Embed query via SentenceTransformers
    2. Search Qdrant for relevant documents
    3. Expand knowledge graph via Neo4j
    4. Synthesize answer via Gemini
    5. Generate citations
    """
    try:
        _ensure_initialized()
    except Exception as e:
        logger.error(f"Failed to initialize GraphRAG pipeline: {e}")
        raise HTTPException(status_code=503, detail=f"GraphRAG pipeline initialization failed: {str(e)}")

    try:
        from backend.rag.models import RagRequest as RagRequestModel

        # Step 1: Embed the query
        query_vector = _embedding_service.embed_query(request.query)

        # Step 2: Search Qdrant
        retrieved_docs = _qdrant_client.search_embeddings(
            collection_name="company_brain_demo",
            query_vector=query_vector,
            tenant_id=request.tenant_id,
            top_k=3
        )

        # Step 3–4: Run the full RAG pipeline (graph expansion + Gemini synthesis)
        rag_request = RagRequestModel(query=request.query, tenant_id=request.tenant_id)
        response = _rag_service.run_graph_rag(
            request=rag_request,
            retrieved_chunks=retrieved_docs,
            seed_nodes=[]
        )

        # Step 5: Generate citations
        graph_context = response.context.graph_context
        retrieved_chunks = response.context.retrieved_chunks

        references = _citation_service.track_sources(
            retrieved_chunks=retrieved_chunks,
            nodes=graph_context.entities,
            edges=graph_context.relationships
        )

        citations = _citation_service.generate_citations(
            answer=response.answer,
            references=references
        )

        # Build sources list from citations
        seen_sources = []
        for cit in citations:
            for src in cit.sources:
                if src.type == "document" and src.source_id not in seen_sources:
                    seen_sources.append(src.source_id)

        sources = [
            SourceItem(index=idx + 1, document_id=src_id)
            for idx, src_id in enumerate(seen_sources)
        ]

        # Build entities list
        entities = [
            EntityItem(
                label=e.get("label", "Entity"),
                node_id=e.get("node_id", ""),
                properties=e.get("properties", {})
            )
            for e in graph_context.entities
        ]

        # Build relationships list
        relationships = [
            RelationshipItem(
                source_id=r.get("source_id", ""),
                target_id=r.get("target_id", ""),
                type=r.get("type", "")
            )
            for r in graph_context.relationships
        ]

        return AskResponse(
            answer=response.answer,
            sources=sources,
            entities=entities,
            relationships=relationships
        )

    except Exception as e:
        logger.error(f"GraphRAG pipeline error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"GraphRAG pipeline error: {str(e)}")


class SystemStats(BaseModel):
    vector_db: str
    graph_db: str
    llm: str
    embedding_model: str
    documents_count: int
    nodes_count: int
    relationships_count: int
    active_pipeline: str
    status: str


@router.get("/stats", response_model=SystemStats, summary="Get real system and database metrics")
async def get_stats():
    """
    Query Qdrant and Neo4j for actual document, node, and relationship counts.
    """
    try:
        _ensure_initialized()
    except Exception as e:
        logger.error(f"Failed to initialize database adapters: {e}")
        return SystemStats(
            vector_db="Qdrant",
            graph_db="Neo4j",
            llm="Gemini 2.5 Flash",
            embedding_model="all-MiniLM-L6-v2",
            documents_count=0,
            nodes_count=0,
            relationships_count=0,
            active_pipeline="GraphRAG",
            status="OFFLINE"
        )

    # 1. Count Qdrant points (documents/chunks)
    documents_count = 0
    try:
        if _qdrant_client.collection_exists("company_brain_demo"):
            # Fetch points count
            res = _qdrant_client.client.count(collection_name="company_brain_demo", exact=True)
            documents_count = res.count
    except Exception as e:
        logger.warning(f"Error querying Qdrant count: {e}")

    # 2. Count Neo4j elements
    nodes_count = 0
    relationships_count = 0
    try:
        with _neo4j_adapter.driver.session() as session:
            nodes_res = session.run("MATCH (n) RETURN count(n) as count").single()
            if nodes_res:
                nodes_count = nodes_res["count"]

            rels_res = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()
            if rels_res:
                relationships_count = rels_res["count"]
    except Exception as e:
        logger.warning(f"Error querying Neo4j count: {e}")

    return SystemStats(
        vector_db="Qdrant",
        graph_db="Neo4j",
        llm="Gemini 2.5 Flash",
        embedding_model="all-MiniLM-L6-v2",
        documents_count=documents_count,
        nodes_count=nodes_count,
        relationships_count=relationships_count,
        active_pipeline="GraphRAG",
        status="ONLINE"
    )


class GraphNodeInfo(BaseModel):
    id: str
    label: str
    type: str
    properties: dict = {}


class GraphEdgeInfo(BaseModel):
    source: str
    target: str
    type: str
    properties: dict = {}


class GraphTopologyResponse(BaseModel):
    nodes: list[GraphNodeInfo]
    edges: list[GraphEdgeInfo]


@router.get("/graph", response_model=GraphTopologyResponse, summary="Get full Neo4j knowledge graph topology")
async def get_graph():
    """
    Fetch all nodes and relationships directly from Neo4j to display in the UI.
    """
    try:
        _ensure_initialized()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not initialized: {str(e)}")

    nodes = []
    edges = []

    try:
        with _neo4j_adapter.driver.session() as session:
            # Fetch nodes
            nodes_query = "MATCH (n) RETURN labels(n) as labels, n.node_id as id, properties(n) as props"
            nodes_res = session.run(nodes_query)
            for record in nodes_res:
                lbl = record["labels"][0] if record["labels"] else "Entity"
                nodes.append(GraphNodeInfo(
                    id=record["id"],
                    label=record["id"],  # Use ID as visual label
                    type=lbl.lower(),    # Return type lowercase for frontend color mapping
                    properties=record["props"] or {}
                ))

            # Fetch edges
            edges_query = "MATCH (n)-[r]->(m) RETURN n.node_id as source, m.node_id as target, type(r) as type, properties(r) as props"
            edges_res = session.run(edges_query)
            for record in edges_res:
                edges.append(GraphEdgeInfo(
                    source=record["source"],
                    target=record["target"],
                    type=record["type"],
                    properties=record["props"] or {}
                ))
    except Exception as e:
        logger.error(f"Error querying Neo4j graph: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error querying graph: {str(e)}")

    return GraphTopologyResponse(nodes=nodes, edges=edges)

