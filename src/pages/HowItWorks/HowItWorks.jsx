import React from 'react';
import PageHeader from '../../components/ui/Layout/PageHeader';
import Card from '../../components/ui/Cards/Card';
import Badge from '../../components/ui/Feedback/Badge';

const HowItWorks = () => {
  const steps = [
    {
      phase: '01',
      title: 'Problem Framing & Query Ingestion',
      tech: 'FastAPI Gateway Router',
      description: 'The user enters a natural language query such as "What caused the payment outage?". The request is authenticated and verified for tenant isolation boundaries before moving downstream.'
    },
    {
      phase: '02',
      title: 'Semantic Vector Retrieval',
      tech: 'Sentence Transformer (all-MiniLM-L6-v2) + Qdrant',
      description: 'The query string is converted to a high-dimensional vector. Qdrant scans indexed document chunks (Cosine similarity) to retrieve text context (e.g. payment_incident.md) containing the outage descriptions.'
    },
    {
      phase: '03',
      title: 'Knowledge Graph Traversal',
      tech: 'Neo4j Bolt connection + BFS Expand',
      description: 'Retrieved document IDs serve as entry seeds to query the Neo4j knowledge database. A depth-3 BFS traversal resolves connected entity nodes (Incident #1001, Slack Thread, Redis Cluster) and causative relations (CAUSED, DISCUSSED_IN).'
    },
    {
      phase: '04',
      title: 'Context Compilation & Grounding',
      tech: 'Orchestration Compiler',
      description: 'Document text chunks and graph relationship paths are combined. The prompt builder structures the context, injecting instructions requiring the LLM to ground its reasoning exclusively in the retrieved facts.'
    },
    {
      phase: '05',
      title: 'LLM Reasoning & Text Synthesis',
      tech: 'Gemini 2.5 Flash',
      description: 'Gemini digests the compiled context. It trace-routes the failure path (Payment Service CAUSED Incident #1001 which is DISCUSSED_IN Slack Thread that REFERENCES Redis Cluster) and synthesizes a step-by-step reasoning reply.'
    },
    {
      phase: '06',
      title: 'Citation Verification & Provenance Mapping',
      tech: 'Citation Service Pipeline',
      description: 'The output is analyzed against the raw source materials. Character spans are mapped back to Qdrant chunks and Neo4j entities, producing confidence-weighted numbered source references.'
    }
  ];

  return (
    <div className="space-y-8 w-full pb-10">
      <PageHeader
        title="System Architecture & Processing Pipeline"
        subtitle="Inside the GraphRAG pipeline: connecting vector documents and structural relations"
      />

      {/* Overview/Problem section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 p-6 border border-ui-border bg-ui-surface/40 space-y-4 shadow-xl">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">The Core Challenge</h3>
          <p className="text-xs text-ui-text-secondary leading-relaxed">
            Standard RAG systems retrieve documents matching semantic keywords, but fail to capture structural connections (e.g. which service causes a specific incident, or who discussed it). 
          </p>
          <p className="text-xs text-ui-text-secondary leading-relaxed">
            <strong>GraphRAG</strong> solves this by combining dense vector indices (Qdrant) with dynamic relationship schemas (Neo4j) to build a unified context block containing both raw text details and structural relational connections.
          </p>
        </Card>

        <Card className="p-6 border border-ui-border bg-ui-surface/40 flex flex-col justify-between shadow-xl">
          <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-2">Connected Pipeline</h3>
          <div className="space-y-2 text-[10px] text-ui-text-secondary">
            <div className="flex justify-between items-center border-b border-ui-divider pb-1">
              <span>Embedding Vector Size</span>
              <span className="font-mono text-white">384 Dim</span>
            </div>
            <div className="flex justify-between items-center border-b border-ui-divider pb-1">
              <span>Similarity Metric</span>
              <span className="font-mono text-white">COSINE</span>
            </div>
            <div className="flex justify-between items-center border-b border-ui-divider pb-1">
              <span>Max BFS Depth</span>
              <span className="font-mono text-white">3 Hops</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Synthesizer Model</span>
              <span className="font-mono text-brand-400">Gemini 2.5 Flash</span>
            </div>
          </div>
          <Badge variant="brand" size="sm" className="mt-4">Production Verified</Badge>
        </Card>
      </div>

      {/* Visual Timeline Section */}
      <Card className="p-6 border border-ui-border bg-ui-surface/40 space-y-6 shadow-xl">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider">Timeline of Execution</h3>
        
        <div className="relative border-l border-brand-500/20 ml-4 pl-8 space-y-8 text-xs">
          {steps.map((s, idx) => (
            <div key={idx} className="relative group">
              {/* timeline node */}
              <span className="absolute -left-[45px] top-0 flex items-center justify-center w-8 h-8 rounded-full bg-slate-900 border border-brand-500/35 text-[10px] font-mono text-brand-400 group-hover:bg-brand-500 group-hover:text-white transition-all select-none">
                {s.phase}
              </span>
              <div className="space-y-1">
                <h4 className="font-extrabold text-white text-xs">{s.title}</h4>
                <span className="text-[10px] font-bold text-brand-400 uppercase tracking-widest block font-mono">{s.tech}</span>
                <p className="text-xs text-ui-text-secondary leading-relaxed max-w-4xl">{s.description}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Core Technical Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-5 border border-ui-border bg-ui-surface/20 space-y-2.5">
          <h4 className="text-xs font-bold text-white uppercase tracking-wide">01. Semantic Retrieval</h4>
          <p className="text-xs text-ui-text-secondary leading-relaxed">
            Uses local embedding maps to query dense documents. Eliminates keyword lookup limits by querying intent.
          </p>
        </Card>
        <Card className="p-5 border border-ui-border bg-ui-surface/20 space-y-2.5">
          <h4 className="text-xs font-bold text-white uppercase tracking-wide">02. BFS Graph Traversals</h4>
          <p className="text-xs text-ui-text-secondary leading-relaxed">
            Performs depth-3 crawls across Neo4j nodes to resolve system-wide causal links and entity maps.
          </p>
        </Card>
        <Card className="p-5 border border-ui-border bg-ui-surface/20 space-y-2.5">
          <h4 className="text-xs font-bold text-white uppercase tracking-wide">03. Provenance Verification</h4>
          <p className="text-xs text-ui-text-secondary leading-relaxed">
            Traces spans and maps confidence weights to guarantee zero-hallucination grounded responses.
          </p>
        </Card>
      </div>
    </div>
  );
};

export default HowItWorks;
