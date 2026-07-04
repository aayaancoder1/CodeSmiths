import React, { useState, useEffect } from 'react';
import MetricCard from '../../components/ui/Cards/MetricCard';
import Card from '../../components/ui/Cards/Card';
import Table from '../../components/ui/Table/Table';
import Loading from '../../components/ui/Feedback/Loading';
import PageHeader from '../../components/ui/Layout/PageHeader';
import { analyticsService } from '../../services/analyticsService';

const Analytics = () => {
  const [stats, setStats] = useState(null);
  const [latencies, setLatencies] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [statsData, latencyData] = await Promise.all([
          analyticsService.getTelemetryStats('7d'),
          analyticsService.getLatencyStats()
        ]);
        setStats(statsData);
        setLatencies(latencyData);
      } catch (err) {
        console.error('Error fetching analytics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
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
      <td className="px-6 py-4 font-mono text-ui-text-tertiary">{item.time}</td>
      <td className="px-6 py-4 text-white font-medium">{item.event}</td>
      <td className="px-6 py-4 font-mono text-ui-text-secondary">{item.endpoint}</td>
      <td className="px-6 py-4 text-brand-400 font-bold">{item.latency}</td>
    </tr>
  );

  return (
    <div className="space-y-6 w-full pb-8">
      <PageHeader 
        title="Telemetry Analytics" 
        subtitle="Detailed system operations, storage usage rates, and latency analytics report"
      />

      {loading ? (
        <Loading message="Fetching aggregate data..." />
      ) : (
        <>
          {/* Metrics Dashboard Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
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
                <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Average API Latency Trend (24h)</h3>
                <span className="text-[10px] text-ui-text-tertiary">Avg: {latencies?.avgLatency}</span>
              </div>
              <div className="h-48 w-full border border-ui-border/50 rounded-xl bg-ui-bg relative overflow-hidden flex items-end p-2">
                {/* SVG Curve chart */}
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
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
                <div className="flex justify-between w-full text-[9px] text-ui-text-tertiary z-10">
                  <span>00:00</span>
                  <span>06:00</span>
                  <span>12:00</span>
                  <span>18:00</span>
                  <span>24:00</span>
                </div>
              </div>
            </Card>

            {/* Chart 2: Storage Ingestion */}
            <Card className="p-5 border border-ui-border bg-ui-surface/40">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Monthly Index Ingestion (GB)</h3>
                <span className="text-[10px] text-ui-text-tertiary">Total: 1,200 GB</span>
              </div>
              <div className="h-48 w-full border border-ui-border/50 rounded-xl bg-ui-bg relative overflow-hidden flex items-end p-2">
                {/* SVG Bar Chart */}
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                  <rect x="5" y="60" width="10" height="40" fill="#28389c" rx="2" />
                  <rect x="25" y="45" width="10" height="55" fill="#28389c" rx="2" />
                  <rect x="45" y="30" width="10" height="70" fill="#5c7cff" rx="2" />
                  <rect x="65" y="20" width="10" height="80" fill="#5c7cff" rx="2" />
                  <rect x="85" y="10" width="10" height="90" fill="#5c7cff" rx="2" />
                </svg>
                <div className="flex justify-between w-full text-[9px] text-ui-text-tertiary z-10 px-1">
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
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Recent Ingestion and Cache Event Activity</h3>
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
