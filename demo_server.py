"""
Lightweight demo server for the GraphRAG integration demo.

Only loads the /api/ask endpoint and a basic health check.
Avoids importing the full backend stack (SQLAlchemy, Redis, Celery, etc.)
which requires infrastructure not needed for the GraphRAG demo path.

Start from project root:
    python demo_server.py
"""
import sys
import os
import logging

# Ensure both project root and backend/ are on the path
# so both `backend.*` and `app.*` imports resolve correctly
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "backend"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Company Brain — GraphRAG Demo",
    description="End-to-end GraphRAG demo: Qdrant + Neo4j + Gemini + Citations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS for frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health Check ---
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "mode": "graphrag-demo"}


# --- Import and register the GraphRAG ask router ---
from backend.app.api.ask import router as ask_router
app.include_router(ask_router)


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting GraphRAG Demo Server on http://localhost:8000")
    logger.info("API docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
