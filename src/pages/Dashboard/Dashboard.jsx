import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MetricCard from '../../components/ui/Cards/MetricCard';
import Card from '../../components/ui/Cards/Card';
import Button from '../../components/ui/Buttons/Button';
import Badge from '../../components/ui/Feedback/Badge';
import Skeleton from '../../components/ui/Feedback/Skeleton';
import PageHeader from '../../components/ui/Layout/PageHeader';
import StatusIndicator from '../../components/ui/Layout/StatusIndicator';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import { dashboardService } from '../../services/dashboardService';
import { useToast } from '../../context/ToastContext';

const Dashboard = () => {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [stats, setStats] = useState(null);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [metricRes, sourcesRes] = await Promise.all([
          dashboardService.getOverviewMetrics(),
          dashboardService.getActiveIngestions()
        ]);
        setStats(metricRes.raw);
        setSources(sourcesRes);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard metrics. Ensure the backend server is running.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [addToast]);

  const MetricSkeleton = () => (
    <div className="p-6 border border-ui-border bg-ui-surface/40 rounded-2xl space-y-4" aria-hidden="true">
      <div className="flex justify-between">
        <Skeleton variant="text" className="w-24 h-3" />
        <Skeleton variant="circle" className="w-6 h-6" />
      </div>
      <Skeleton variant="text" className="w-16 h-8 mt-2" />
    </div>
  );

  return (
    <div className="space-y-6 w-full pb-8">
      {/* Header */}
      <PageHeader
        title="AI Company Brain"
        subtitle="Operations center monitoring Vector DB, Graph DB, and the GraphRAG pipeline"
      />

      {/* Demo Banner */}
      <div className="p-4 bg-brand-500/10 border border-brand-500/20 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-lg backdrop-blur-md">
        <div className="flex items-center gap-3">
          <span className="text-2xl select-none">💡</span>
          <div>
            <h4 className="text-xs font-extrabold text-white">GraphRAG Demo Environment Active</h4>
            <p className="text-[10px] text-ui-text-secondary leading-relaxed">System loaded with Slack channels, incident reports, and Redis outage logs.</p>
          </div>
        </div>
        <Button variant="primary" size="sm" onClick={() => navigate('/chat')} className="shrink-0 font-bold shadow-lg shadow-brand-500/20">
          Query Chat UI 💬
        </Button>
      </div>

      {error && !loading && (
        <EmptyState
          title="FastAPI Server Offline"
          description={error}
          action={
            <Button
              variant="primary"
              size="sm"
              onClick={() => window.location.reload()}
            >
              Retry Connection
            </Button>
          }
        />
      )}

      {/* Real Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => <MetricSkeleton key={i} />)
        ) : (
          <>
            <MetricCard
              title="Indexed Chunks"
              value={stats?.documents_count ?? '0'}
              change="Stored in Qdrant"
              changeType="positive"
              icon="📂"
            />
            <MetricCard
              title="Knowledge Graph Nodes"
              value={stats?.nodes_count ?? '0'}
              change="Synced in Neo4j"
              changeType="positive"
              icon="🕸️"
            />
            <MetricCard
              title="Graph Relationships"
              value={stats?.relationships_count ?? '0'}
              change="Connected mappings"
              changeType="positive"
              icon="🔗"
            />
            <MetricCard
              title="Pipeline Status"
              value={stats?.status ?? 'OFFLINE'}
              change="FastAPI Endpoint"
              changeType={stats?.status === 'ONLINE' ? 'positive' : 'negative'}
              icon="🔌"
            />
          </>
        )}
      </div>

      {/* Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Visual Pipeline flow (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6 border border-ui-border bg-ui-surface/40 space-y-6 shadow-xl">
            <div className="flex justify-between items-center pb-3 border-b border-ui-divider">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-brand-500" /> GraphRAG Pipeline Visualization
              </h3>
              <Badge variant="brand" size="sm">Active Pipeline: {stats?.active_pipeline ?? 'GraphRAG'}</Badge>
            </div>

            {/* Premium Pipeline visualization flow */}
            <div className="space-y-4">
              <p className="text-xs text-ui-text-secondary leading-relaxed">
                When a query is received, the system retrieves relevant vector documents, expands local knowledge graph relationships, constructs a grounded context prompt, and generates a cited answer.
              </p>
              
              <div className="bg-ui-bg/70 border border-ui-border rounded-2xl p-6 space-y-6">
                {/* Visual flowchart using css layout */}
                <div className="grid grid-cols-7 items-center text-center gap-1">
                  <div className="p-2.5 bg-slate-900 border border-ui-border rounded-xl">
                    <span className="text-base">💬</span>
                    <span className="text-[9px] font-extrabold text-white block mt-1">User Query</span>
                  </div>
                  <div className="text-ui-text-tertiary font-bold text-xs select-none">➔</div>
                  <div className="p-2.5 bg-brand-500/10 border border-brand-500/20 rounded-xl">
                    <span className="text-base">⚙️</span>
                    <span className="text-[9px] font-extrabold text-brand-400 block mt-1">Embeddings</span>
                  </div>
                  <div className="text-ui-text-tertiary font-bold text-xs select-none">➔</div>
                  <div className="p-2.5 bg-brand-500/10 border border-brand-500/20 rounded-xl">
                    <span className="text-base">📂</span>
                    <span className="text-[9px] font-extrabold text-brand-400 block mt-1">Qdrant Scan</span>
                  </div>
                  <div className="text-ui-text-tertiary font-bold text-xs select-none">➔</div>
                  <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
                    <span className="text-base">🕸️</span>
                    <span className="text-[9px] font-extrabold text-emerald-400 block mt-1">Neo4j BFS</span>
                  </div>
                </div>

                <div className="grid grid-cols-7 items-center text-center gap-1">
                  <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl col-span-1">
                    <span className="text-base">🕸️</span>
                    <span className="text-[9px] font-extrabold text-emerald-400 block mt-1">Neo4j BFS</span>
                  </div>
                  <div className="text-ui-text-tertiary font-bold text-xs select-none">➔</div>
                  <div className="p-2.5 bg-amber-500/10 border border-amber-500/20 rounded-xl">
                    <span className="text-base">🔍</span>
                    <span className="text-[9px] font-extrabold text-amber-400 block mt-1">BFS Expand</span>
                  </div>
                  <div className="text-ui-text-tertiary font-bold text-xs select-none">➔</div>
                  <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
                    <span className="text-base">🤖</span>
                    <span className="text-[9px] font-extrabold text-indigo-400 block mt-1">Gemini 2.5</span>
                  </div>
                  <div className="text-ui-text-tertiary font-bold text-xs select-none">➔</div>
                  <div className="p-2.5 bg-slate-900 border border-ui-border rounded-xl">
                    <span className="text-base">📄</span>
                    <span className="text-[9px] font-extrabold text-white block mt-1">Cited Response</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Connected Data Sources */}
          <Card className="p-6 border border-ui-border bg-ui-surface/40 shadow-xl">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-4">
              Connected Knowledge base Sources
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {sources.map((source, idx) => (
                <div
                  key={idx}
                  className="flex flex-col justify-between p-4 rounded-xl border border-ui-border bg-ui-bg/50 hover:bg-ui-bg/70 transition-all min-h-[110px]"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-lg select-none">{source.icon}</span>
                    <h4 className="text-[11px] font-bold text-ui-text-primary truncate">{source.name}</h4>
                  </div>
                  <div className="mt-4 flex items-center justify-between">
                    <span className="text-[9px] text-ui-text-tertiary font-mono">{source.count}</span>
                    <StatusIndicator status="active" label="Indexed" />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Infrastructures Connection info (1 col) */}
        <div className="space-y-6">
          <Card className="p-6 border border-ui-border bg-ui-surface/40 space-y-4 shadow-xl">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">
              Connected Infrastructure
            </h3>
            <div className="space-y-3.5 text-xs">
              <div className="flex justify-between items-center border-b border-ui-divider pb-2.5">
                <span className="text-ui-text-secondary">Qdrant Client</span>
                <span className="font-mono text-ui-text-tertiary text-[10px]">http://localhost:6333</span>
              </div>
              <div className="flex justify-between items-center border-b border-ui-divider pb-2.5">
                <span className="text-ui-text-secondary">Neo4j Bolt</span>
                <span className="font-mono text-ui-text-tertiary text-[10px]">bolt://localhost:7687</span>
              </div>
              <div className="flex justify-between items-center border-b border-ui-divider pb-2.5">
                <span className="text-ui-text-secondary">Vector Size / Dim</span>
                <span className="font-mono text-ui-text-tertiary text-[10px]">384 / Cosine</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-ui-text-secondary">Model Version</span>
                <span className="font-mono text-brand-400 text-[10px]">gemini-2.5-flash</span>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-ui-border bg-ui-surface/40 space-y-4 shadow-xl">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">
              Verification Suite
            </h3>
            <p className="text-xs text-ui-text-secondary leading-relaxed">
              Verify end-to-end GraphRAG answering with full citations by clicking below.
            </p>
            <Button
              variant="outline"
              size="sm"
              className="w-full justify-between items-center font-bold text-xs"
              onClick={() => navigate('/chat')}
            >
              <span>Ask outage query</span>
              <span>➔</span>
            </Button>
          </Card>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
