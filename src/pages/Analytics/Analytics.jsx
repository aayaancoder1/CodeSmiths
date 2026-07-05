import React, { useState, useEffect } from 'react';
import MetricCard from '../../components/ui/Cards/MetricCard';
import Card from '../../components/ui/Cards/Card';
import Table from '../../components/ui/Table/Table';
import Loading from '../../components/ui/Feedback/Loading';
import Skeleton from '../../components/ui/Feedback/Skeleton';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import Button from '../../components/ui/Buttons/Button';
import PageHeader from '../../components/ui/Layout/PageHeader';
import { analyticsService } from '../../services/analyticsService';
import { useToast } from '../../context/ToastContext';

const Analytics = () => {
  const { addToast } = useToast();
  const [stats, setStats] = useState(null);
  const [latencies, setLatencies] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      const [statsData, latencyData] = await Promise.all([
        analyticsService.getTelemetryStats('7d'),
        analyticsService.getLatencyStats()
      ]);
      setStats(statsData);
      setLatencies(latencyData);
    } catch (err) {
      console.error('Error fetching analytics:', err);
      setError('Failed to load telemetry data.');
      addToast({
        message: 'Analytics Error',
        description: 'Failed to fetch system telemetry data.',
        variant: 'danger'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const tableHeaders = [
    { label: 'Timestamp', key: 'time' },
    { label: 'Event', key: 'event' },
    { label: 'Endpoint', key: 'endpoint' },
    { label: 'Latency', key: 'latency' }
  ];

  const tableData = [
    { time: '2026-07-04 16:02:18', event: 'GraphQL Node Query', endpoint: '/api/v1/graphql', latency: '124ms' },
    { time: '2026-07-04 15:58:45', event: 'Slack Sync Batch Ingest', endpoint: '/api/v1/sync/slack', latency: '402ms' },
    { time: '2026-07-04 15:30:12', event: 'Vector Embedding Create', endpoint: '/api/v1/embeddings', latency: '88ms' },
    { time: '2026-07-04 14:12:00', event: 'Notion Sync Ingest', endpoint: '/api/v1/sync/notion', latency: '312ms' }
  ];

  const renderRow = (item, idx) => (
    <tr key={idx} className="hover:bg-ui-surfaceHover transition-colors border-b border-ui-divider last:border-0 text-xs">
      <td className="px-6 py-4 font-mono text-ui-text-tertiary">
        <time>{item.time}</time>
      </td>
      <td className="px-6 py-4 text-white font-medium">{item.event}</td>
      <td className="px-6 py-4 font-mono text-ui-text-secondary">{item.endpoint}</td>
      <td className="px-6 py-4 text-brand-400 font-bold">{item.latency}</td>
    </tr>
  );

  // Metric skeleton
  const MetricSkeleton = () => (
    <div className="p-5 border border-ui-border bg-ui-surface/40 rounded-xl space-y-4" aria-hidden="true">
      <div className="flex justify-between">
        <Skeleton variant="text" className="w-28 h-3" />
        <Skeleton variant="circle" className="w-6 h-6" />
      </div>
      <Skeleton variant="text" className="w-20 h-8 mt-2" />
    </div>
  );

  return (
    <div className="space-y-6 w-full pb-8">
      <PageHeader
        title="Telemetry Analytics"
        subtitle="Detailed system operations, storage usage rates, and latency analytics report"
      />

      {loading ? (
        <>
          {/* Skeleton metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" aria-label="Loading metrics" aria-busy="true">
            {Array.from({ length: 4 }).map((_, i) => <MetricSkeleton key={i} />)}
          </div>

          {/* Chart skeletons */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="p-5 border border-ui-border bg-ui-surface/40">
              <Skeleton variant="text" className="w-48 h-3 mb-4" aria-hidden="true" />
              <Skeleton variant="rect" className="h-48 rounded-xl" aria-hidden="true" />
            </Card>
            <Card className="p-5 border border-ui-border bg-ui-surface/40">
              <Skeleton variant="text" className="w-48 h-3 mb-4" aria-hidden="true" />
              <Skeleton variant="rect" className="h-48 rounded-xl" aria-hidden="true" />
            </Card>
          </div>

          <Loading message="Fetching aggregate data..." />
        </>
      ) : error ? (
        <EmptyState
          title="Failed to Load Analytics"
          description={error}
          action={
            <Button variant="primary" size="sm" onClick={fetchAnalytics}>
              Retry
            </Button>
          }
        />
      ) : (
        <>
          {/* Metrics Dashboard Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" aria-label="System metrics">
            <MetricCard title="Total Storage Indexed" value={stats?.storageSaved || '0'} change="+45 GB" changeType="positive" icon="💾" />
            <MetricCard title="Queries Answered" value={stats?.queriesCount || '0'} change="+12.4k" changeType="positive" icon="✔️" />
            <MetricCard title="Active Connectors" value={stats?.activeIntegrations || '0'} change="Optimal" changeType="neutral" icon="🔌" />
            <MetricCard title="System Availability" value={stats?.dbHealth || '0%'} change="99.99% uptime" changeType="positive" icon="❤️" />
          </div>

          {/* SVG Latency and Ingestion Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* Chart 1: Latency */}
            <Card className="p-5 border border-ui-border bg-ui-surface/40">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
                  Average API Latency Trend (24h)
                </h2>
                <span className="text-[10px] text-ui-text-tertiary" aria-live="polite">
                  Avg: {latencies?.avgLatency}
                </span>
              </div>
              <div
                className="h-48 w-full border border-ui-border/50 rounded-xl bg-ui-bg relative overflow-hidden flex items-end p-2"
                role="img"
                aria-label={`API latency trend chart. Average: ${latencies?.avgLatency}, P95: ${latencies?.p95Latency}, P99: ${latencies?.p99Latency}`}
              >
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
                  <path
                    d="M 0 80 Q 25 50 50 60 T 100 20 L 100 100 L 0 100 Z"
                    fill="url(#latencyGrad)"
                    opacity="0.15"
                  />
                  <path
                    d="M 0 80 Q 25 50 50 60 T 100 20"
                    fill="none"
                    stroke="#5c7cff"
                    strokeWidth="2.5"
                  />
                  <defs>
                    <linearGradient id="latencyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stopColor="#5c7cff" />
                      <stop offset="100%" stopColor="#5c7cff" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="flex justify-between w-full text-[9px] text-ui-text-tertiary z-10" aria-hidden="true">
                  <span>00:00</span>
                  <span>06:00</span>
                  <span>12:00</span>
                  <span>18:00</span>
                  <span>24:00</span>
                </div>
              </div>
              {/* Latency stats summary */}
              <div className="mt-3 grid grid-cols-3 gap-2 text-center">
                {[
                  { label: 'Avg', value: latencies?.avgLatency },
                  { label: 'P95', value: latencies?.p95Latency },
                  { label: 'P99', value: latencies?.p99Latency }
                ].map((stat) => (
                  <div key={stat.label} className="rounded-lg border border-ui-border bg-ui-bg/50 p-2">
                    <p className="text-[10px] text-ui-text-tertiary uppercase tracking-wider">{stat.label}</p>
                    <p className="text-xs font-bold text-brand-400 mt-0.5">{stat.value}</p>
                  </div>
                ))}
              </div>
            </Card>

            {/* Chart 2: Storage Ingestion */}
            <Card className="p-5 border border-ui-border bg-ui-surface/40">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
                  Monthly Index Ingestion (GB)
                </h2>
                <span className="text-[10px] text-ui-text-tertiary">Total: 1,200 GB</span>
              </div>
              <div
                className="h-48 w-full border border-ui-border/50 rounded-xl bg-ui-bg relative overflow-hidden flex items-end p-2"
                role="img"
                aria-label="Monthly storage ingestion bar chart. Feb through Jun, showing growth from ~40GB to ~90GB."
              >
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
                  <rect x="5" y="60" width="10" height="40" fill="#28389c" rx="2" />
                  <rect x="25" y="45" width="10" height="55" fill="#28389c" rx="2" />
                  <rect x="45" y="30" width="10" height="70" fill="#5c7cff" rx="2" />
                  <rect x="65" y="20" width="10" height="80" fill="#5c7cff" rx="2" />
                  <rect x="85" y="10" width="10" height="90" fill="#5c7cff" rx="2" />
                </svg>
                <div className="flex justify-between w-full text-[9px] text-ui-text-tertiary z-10 px-1" aria-hidden="true">
                  <span>Feb</span>
                  <span>Mar</span>
                  <span>Apr</span>
                  <span>May</span>
                  <span>Jun</span>
                </div>
              </div>
            </Card>
          </div>

          {/* Activity Log Table */}
          <div className="space-y-3">
            <h2 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
              Recent Ingestion and Cache Event Activity
            </h2>
            <Table
              headers={tableHeaders}
              data={tableData}
              renderRow={renderRow}
              totalPages={1}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default Analytics;
