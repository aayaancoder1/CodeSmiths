import React, { useState } from 'react';
import MetricCard from '../../components/ui/Cards/MetricCard';
import Card from '../../components/ui/Cards/Card';
import Button from '../../components/ui/Buttons/Button';
import SearchInput from '../../components/ui/Inputs/SearchInput';
import Badge from '../../components/ui/Feedback/Badge';
import PageHeader from '../../components/ui/Layout/PageHeader';
import StatusIndicator from '../../components/ui/Layout/StatusIndicator';

const Dashboard = () => {
  const [searchValue, setSearchValue] = useState('');

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

  const connectedSources = [
    { name: 'Google Drive', icon: '📂', status: 'connected', count: '1,420 docs' },
    { name: 'Notion Workspace', icon: '📝', status: 'connected', count: '458 pages' },
    { name: 'Slack Channels', icon: '💬', status: 'connected', count: '12 channels' },
    { name: 'GitHub Codebase', icon: '💻', status: 'connected', count: '8 repos' }
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

  return (
    <div className="space-y-6 w-full pb-8">
      {/* Header */}
      <PageHeader 
        title="Operations Hub" 
        subtitle="Unified intelligence dashboard & connected knowledge bases"
      />

      {/* Analytics Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Total Indexed Nodes" value="84,290" change="+12.4%" changeType="positive" icon="🕸️" />
        <MetricCard title="System Queries (24h)" value="1,842" change="+3.8%" changeType="positive" icon="⚡" />
        <MetricCard title="Ingestion Latency" value="108ms" change="-12ms" changeType="positive" icon="⚙️" />
        <MetricCard title="Connected Sources" value="4 / 6" change="Online" changeType="neutral" icon="🔌" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Side Column (2 cols wide on desktop) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Search Bar & Quick Actions */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-3">Enterprise Brain Search</h3>
            <div className="flex flex-col sm:flex-row gap-3">
              <SearchInput 
                value={searchValue}
                onChange={(val) => setSearchValue(val)}
                onClear={() => setSearchValue('')}
                placeholder="Search connected knowledge networks..."
              />
              <Button 
                onClick={() => window.location.href = `/search?q=${encodeURIComponent(searchValue)}`}
                variant="primary"
                className="shrink-0"
              >
                Execute Query
              </Button>
            </div>

            {/* Quick Actions Grid */}
            <div className="mt-5 pt-4 border-t border-ui-divider">
              <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block mb-3">Quick Navigation</span>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {quickActions.map((action, idx) => (
                  <button
                    key={idx}
                    onClick={() => window.location.href = action.path}
                    className="flex flex-col items-center justify-center p-3 rounded-xl border border-ui-border bg-ui-bg hover:bg-ui-surfaceHover hover:border-ui-borderHover transition-all text-center gap-1.5 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
                  >
                    <span className="text-lg select-none">{action.icon}</span>
                    <span className="text-xs font-semibold text-ui-text-secondary">{action.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </Card>

          {/* Connected Sources Grid */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-4">Connected Sources</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {connectedSources.map((source, idx) => (
                <div 
                  key={idx}
                  className="flex items-center justify-between p-3.5 rounded-xl border border-ui-border bg-ui-bg"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xl select-none">{source.icon}</span>
                    <div>
                      <h4 className="text-xs font-bold text-ui-text-primary">{source.name}</h4>
                      <p className="text-[10px] text-ui-text-tertiary">{source.count}</p>
                    </div>
                  </div>
                  <StatusIndicator status="active" label="Syncing" />
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Right Side Column (1 col wide on desktop) */}
        <div className="space-y-6">
          {/* Recent Searches */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-3">Recent Inquiries</h3>
            <div className="space-y-2">
              {recentSearches.map((query, idx) => (
                <div 
                  key={idx}
                  onClick={() => window.location.href = `/search?q=${encodeURIComponent(query)}`}
                  className="text-xs text-ui-text-secondary hover:text-brand-400 cursor-pointer p-2 rounded-lg bg-ui-bg hover:bg-ui-surface transition-all truncate border border-transparent hover:border-ui-border"
                >
                  🔍 {query}
                </div>
              ))}
            </div>
          </Card>

          {/* Notifications */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Alerts & Warnings</h3>
              <Badge variant="warning" size="sm">2 Active</Badge>
            </div>
            <div className="space-y-3">
              {notifications.map((notif, idx) => (
                <div key={idx} className="p-3 rounded-lg bg-ui-bg border border-ui-border text-xs space-y-1">
                  <h4 className="font-bold text-ui-text-primary flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                    {notif.title}
                  </h4>
                  <p className="text-ui-text-secondary text-[11px] leading-relaxed">{notif.description}</p>
                </div>
              ))}
            </div>
          </Card>

          {/* Recent System Activity */}
          <Card className="p-5 border border-ui-border bg-ui-surface/40">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-3">Activity Monitor</h3>
            <div className="space-y-3">
              {recentActivities.map((act, idx) => (
                <div key={idx} className="flex justify-between items-start gap-2 border-b border-ui-divider pb-2.5 last:border-0 last:pb-0">
                  <div className="space-y-0.5">
                    <p className="text-xs text-ui-text-secondary leading-snug">{act.text}</p>
                    <span className="text-[10px] text-ui-text-tertiary block">{act.time}</span>
                  </div>
                  <Badge variant={act.status === 'success' ? 'success' : act.status === 'warning' ? 'warning' : 'info'} size="sm">
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
