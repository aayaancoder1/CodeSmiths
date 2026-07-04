from .models import BrainDocument, BrainQuery, BrainOutput
from .pipeline import ExecutionPipeline
from .workflow import BrainWorkflow

class BrainOrchestrator:
    """
    Main integrated coordinator routing calls between workflows and pipeline executors.
    """

    def __init__(self, pipeline: ExecutionPipeline, workflow: BrainWorkflow):
        self.pipeline = pipeline
        self.workflow = workflow

    def ingest(self, doc: BrainDocument) -> None:
        self.pipeline.run_ingestion_pipeline(doc)
        self.workflow.log_state(doc.document_id, "ingestion", {"status": "success"})

    def query(self, query: BrainQuery) -> BrainOutput:
        output = self.pipeline.run_retrieval_pipeline(query)
        self.workflow.log_state(query.query, "query", {"status": "success", "latency": output.metrics})
        return output
