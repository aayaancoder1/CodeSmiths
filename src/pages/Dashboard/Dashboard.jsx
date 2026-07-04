import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MetricCard from '../../components/ui/Cards/MetricCard';
import Card from '../../components/ui/Cards/Card';
import Button from '../../components/ui/Buttons/Button';
import SearchInput from '../../components/ui/Inputs/SearchInput';
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
  const [searchValue, setSearchValue] = useState('');
  const [metrics, setMetrics] = useState(null);
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
        setMetrics(metricRes);
        setSources(sourcesRes);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again.');
        addToast({
          message: 'Dashboard Error',
          description: 'Failed to load system metrics. Retrying...',
          variant: 'warning'
        });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [addToast]);

  const quickActions = [
    { label: 'New Search Query', icon: '🔍', path: '/search' },
    { label: 'Open Chat Workspace', icon: '💬', path: '/chat' },
    { label: 'Knowledge Graph', icon: '🕸️', path: '/knowledge-graph' },
    { label: 'Connected Repos', icon: '🔗', path: '/admin' }
  ];

  const recentSearches = [
    'Q3 Ingestion pipeline fail reason',
    'security tokens for AWS microservices',
    'employee onboarding checklist docs',
    'Vite optimization guidelines'
  ];

  const recentActivities = [
    { text: 'Slack Ingestion synced successfully', time: '10 mins ago', status: 'success' },
    { text: 'Query cache size limit exceeded', time: '1 hour ago', status: 'warning' },
    { text: 'Re-indexing Knowledge Graph Node #208', time: '3 hours ago', status: 'info' }
  ];

  const notifications = [
    { title: 'Ingestion Completed', description: 'GitHub repo "codesmiths-core" fully indexed.', type: 'info' },
    { title: 'Pipeline Alert', description: 'Daily backup script warning for GDrive sync.', type: 'warning' }
  ];

  const handleSearch = () => {
    if (searchValue.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchValue)}`);
    }
  };

  // Metric skeleton placeholders
  const MetricSkeleton = () => (
    <div className="p-5 border border-ui-border bg-ui-surface/40 rounded-xl space-y-4" aria-hidden="true">
      <div className="flex justify-between">
        <Skeleton variant="text" className="w-28 h-3" />
        <Skeleton variant="circle" className="w-6 h-6" />
      </div>
      <Skeleton variant="text" className="w-20 h-8 mt-2" />
    </div>
  );

  // Source skeleton
  const SourceSkeleton = () => (
    <div className="flex items-center justify-between p-3.5 rounded-xl border border-ui-border bg-ui-bg" aria-hidden="true">
      <div className="flex items-center gap-3">
        <Skeleton variant="circle" className="w-8 h-8" />
        <div className="space-y-1.5">
          <Skeleton variant="text" className="w-24 h-3" />
          <Skeleton variant="text" className="w-16 h-2.5" />
        </div>
      </div>
      <Skeleton variant="text" className="w-14 h-3" />
    </div>
  );

  return (
    <div className="space-y-6 w-full pb-8">
      {/* Header */}
      <PageHeader
        title="Operations Hub"
        subtitle="Unified intelligence dashboard & connected knowledge bases"
      />

      {/* Error State */}
      {error && !loading && (
        <EmptyState
          title="Failed to Load Dashboard"
          description={error}
          action={
            <Button
              variant="primary"
              size="sm"
              onClick={() => window.location.reload()}
            >
              Retry
            </Button>
          }
        />
      )}

      {/* Analytics Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" aria-label="Key metrics">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => <MetricSkeleton key={i} />)
        ) : (
          <>
            <MetricCard
              title="Total Indexed Nodes"
              value={metrics?.indexedNodes || '0'}
              change="+12.4%"
              changeType="positive"
              icon="🕸️"
            />
            <MetricCard
              title="System Queries (24h)"
              value={metrics?.queriesCount || '0'}
              change="+3.8%"
              changeType="positive"
              icon="⚡"
            />
            <MetricCard
              title="Ingestion Latency"
              value={metrics?.latency || '0ms'}
              change="-12ms"
              changeType="positive"
              icon="⚙️"
            />
            <MetricCard
              title="Connected Sources"
              value={metrics?.connectedCount || '0'}
              change="Online"
              changeType="neutral"
              icon="🔌"
            />
          </>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Side Column (2 cols wide on desktop) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Search Bar & Quick Actions */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-3">
              Enterprise Brain Search
            </h3>
            <div className="flex flex-col sm:flex-row gap-3">
              <SearchInput
                value={searchValue}
                onChange={(val) => setSearchValue(val)}
                onClear={() => setSearchValue('')}
                placeholder="Search connected knowledge networks..."
                aria-label="Search knowledge base"
              />
              <Button
                onClick={handleSearch}
                variant="primary"
                className="shrink-0"
                disabled={!searchValue.trim()}
              >
                Execute Query
              </Button>
            </div>

            {/* Quick Actions Grid */}
            <div className="mt-5 pt-4 border-t border-ui-divider">
              <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block mb-3">
                Quick Navigation
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3" role="navigation" aria-label="Quick actions">
                {quickActions.map((action, idx) => (
                  <button
                    key={idx}
                    onClick={() => navigate(action.path)}
                    className="flex flex-col items-center justify-center p-3 rounded-xl border border-ui-border bg-ui-bg hover:bg-ui-surfaceHover hover:border-ui-borderHover transition-all text-center gap-1.5 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50"
                    aria-label={`Navigate to ${action.label}`}
                  >
                    <span className="text-lg select-none" aria-hidden="true">{action.icon}</span>
                    <span className="text-xs font-semibold text-ui-text-secondary">{action.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </Card>

          {/* Connected Sources Grid */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-4">
              Connected Sources
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {loading ? (
                Array.from({ length: 4 }).map((_, i) => <SourceSkeleton key={i} />)
              ) : sources.length === 0 ? (
                <div className="col-span-2">
                  <EmptyState
                    title="No sources connected"
                    description="Connect data sources from the Admin panel to start indexing."
                  />
                </div>
              ) : (
                sources.map((source, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3.5 rounded-xl border border-ui-border bg-ui-bg"
                    role="listitem"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xl select-none" aria-hidden="true">{source.icon}</span>
                      <div>
                        <h4 className="text-xs font-bold text-ui-text-primary">{source.name}</h4>
                        <p className="text-[10px] text-ui-text-tertiary">{source.count}</p>
                      </div>
                    </div>
                    <StatusIndicator status="active" label="Syncing" />
                  </div>
                ))
              )}
            </div>
          </Card>
        </div>

        {/* Right Side Column (1 col wide on desktop) */}
        <div className="space-y-6">
          {/* Recent Searches */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-3">
              Recent Inquiries
            </h3>
            <div className="space-y-2" role="list" aria-label="Recent searches">
              {recentSearches.map((query, idx) => (
                <button
                  key={idx}
                  onClick={() => navigate(`/search?q=${encodeURIComponent(query)}`)}
                  className="w-full text-left text-xs text-ui-text-secondary hover:text-brand-400 cursor-pointer p-2 rounded-lg bg-ui-bg hover:bg-ui-surface transition-all truncate border border-transparent hover:border-ui-border focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50"
                  aria-label={`Search for: ${query}`}
                >
                  <span aria-hidden="true">🔍 </span>{query}
                </button>
              ))}
            </div>
          </Card>

          {/* Notifications */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
                Alerts & Warnings
              </h3>
              <Badge variant="warning" size="sm">2 Active</Badge>
            </div>
            <div className="space-y-3" role="list" aria-label="System alerts">
              {notifications.map((notif, idx) => (
                <div key={idx} className="p-3 rounded-lg bg-ui-bg border border-ui-border text-xs space-y-1" role="listitem">
                  <h4 className="font-bold text-ui-text-primary flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500" aria-hidden="true" />
                    {notif.title}
                  </h4>
                  <p className="text-ui-text-secondary text-[11px] leading-relaxed">{notif.description}</p>
                </div>
              ))}
            </div>
          </Card>

          {/* Recent System Activity */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-3">
              Activity Monitor
            </h3>
            <div className="space-y-3" role="list" aria-label="Recent system activity">
              {recentActivities.map((act, idx) => (
                <div key={idx} className="flex justify-between items-start gap-2 border-b border-ui-divider pb-2.5 last:border-0 last:pb-0" role="listitem">
                  <div className="space-y-0.5">
                    <p className="text-xs text-ui-text-secondary leading-snug">{act.text}</p>
                    <span className="text-[10px] text-ui-text-tertiary block">
                      <time>{act.time}</time>
                    </span>
                  </div>
                  <Badge
                    variant={act.status === 'success' ? 'success' : act.status === 'warning' ? 'warning' : 'info'}
                    size="sm"
                  >
                    {act.status}
                  </Badge>
                </div>
              ))}
            </div>
          </Card>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
