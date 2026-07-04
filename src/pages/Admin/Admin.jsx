import React, { useState, useEffect } from 'react';
import Table from '../../components/ui/Table/Table';
import Badge from '../../components/ui/Feedback/Badge';
import Button from '../../components/ui/Buttons/Button';
import Avatar from '../../components/ui/Feedback/Avatar';
import Loading from '../../components/ui/Feedback/Loading';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import PageHeader from '../../components/ui/Layout/PageHeader';
import Tabs from '../../components/ui/Layout/Tabs';
import StatusIndicator from '../../components/ui/Layout/StatusIndicator';
import Card from '../../components/ui/Cards/Card';
import Divider from '../../components/ui/Layout/Divider';
import { adminService } from '../../services/adminService';
import { useToast } from '../../context/ToastContext';

const Admin = () => {
  const { addToast } = useToast();
  const [contributors, setContributors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('users');
  const [savingSettings, setSavingSettings] = useState(false);

  const fetchAdminData = async () => {
    setLoading(true);
    setError(null);
    try {
      const users = await adminService.getContributors();
      setContributors(users);
    } catch (err) {
      console.error('Error fetching admin data:', err);
      setError('Failed to load contributor data.');
      addToast({
        message: 'Admin Error',
        description: 'Failed to load workspace contributors.',
        variant: 'danger'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleRevokeAccess = async (user) => {
    try {
      await adminService.updateContributorPermissions(user.id, { revoked: true });
      addToast({
        message: 'Access Revoked',
        description: `${user.name}'s access has been revoked.`,
        variant: 'warning'
      });
    } catch (err) {
      addToast({
        message: 'Action Failed',
        description: 'Could not update permissions. Please try again.',
        variant: 'danger'
      });
    }
  };

  const handleSaveSettings = async () => {
    setSavingSettings(true);
    try {
      // Placeholder — wire to settings service when available
      await new Promise((resolve) => setTimeout(resolve, 800));
      addToast({
        message: 'Settings Saved',
        description: 'System configuration has been updated successfully.',
        variant: 'success'
      });
    } catch (err) {
      addToast({
        message: 'Save Failed',
        description: 'Could not save settings. Please try again.',
        variant: 'danger'
      });
    } finally {
      setSavingSettings(false);
    }
  };

  const tabs = [
    { id: 'users', label: 'Users & Roles' },
    { id: 'sources', label: 'Connected Sources' },
    { id: 'health', label: 'System Health' },
    { id: 'logs', label: 'Audit Logs' },
    { id: 'settings', label: 'Settings' }
  ];

  const userTableHeaders = [
    { label: 'Member', key: 'name' },
    { label: 'Role', key: 'role' },
    { label: 'Status', key: 'status' },
    { label: 'Actions', key: 'actions' }
  ];

  const renderUserRow = (user) => (
    <tr key={user.id} className="hover:bg-ui-surfaceHover transition-colors border-b border-ui-divider last:border-0">
      <td className="px-6 py-4">
        <div className="flex items-center gap-3">
          <Avatar name={user.name} size="sm" status="online" />
          <div>
            <p className="text-xs font-bold text-ui-text-primary">{user.name}</p>
            <p className="text-[10px] text-ui-text-tertiary">{user.name.toLowerCase()}@codesmiths.ai</p>
          </div>
        </div>
      </td>
      <td className="px-6 py-4 text-xs text-ui-text-secondary">{user.role}</td>
      <td className="px-6 py-4">
        <Badge variant="success" size="sm">{user.status}</Badge>
      </td>
      <td className="px-6 py-4">
        <div className="flex gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => addToast({ message: 'Edit Member', description: `Edit permissions for ${user.name}.`, variant: 'info' })}
            aria-label={`Edit permissions for ${user.name}`}
          >
            Edit
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="text-ui-danger-text hover:text-ui-danger-solid"
            onClick={() => handleRevokeAccess(user)}
            aria-label={`Revoke access for ${user.name}`}
          >
            Revoke
          </Button>
        </div>
      </td>
    </tr>
  );

  const connectedSources = [
    { name: 'Google Drive', icon: '📂', status: 'connected', syncFreq: 'Every 2 hours', lastSync: '8 mins ago' },
    { name: 'Notion Workspace', icon: '📝', status: 'connected', syncFreq: 'Every 4 hours', lastSync: '1 hour ago' },
    { name: 'Slack Channels', icon: '💬', status: 'connected', syncFreq: 'Real-time', lastSync: 'Just now' },
    { name: 'GitHub Repos', icon: '💻', status: 'connected', syncFreq: 'On push event', lastSync: '3 hours ago' },
    { name: 'Confluence', icon: '🗂️', status: 'disconnected', syncFreq: 'N/A', lastSync: 'Never' },
    { name: 'Jira Board', icon: '🎯', status: 'disconnected', syncFreq: 'N/A', lastSync: 'Never' }
  ];

  const systemHealthMetrics = [
    { name: 'CPU Usage', value: '24%', level: 'success', bar: 24 },
    { name: 'Memory Usage', value: '61%', level: 'warning', bar: 61 },
    { name: 'Storage Index', value: '48%', level: 'success', bar: 48 },
    { name: 'API Gateway Load', value: '18%', level: 'success', bar: 18 }
  ];

  const auditLogs = [
    { user: 'Aayaan', action: 'Updated ingestion pipeline config', time: '2026-07-04 16:32', type: 'config' },
    { user: 'Thanmayee', action: 'Deployed new UI build to staging', time: '2026-07-04 15:10', type: 'deploy' },
    { user: 'Kishan', action: 'Added new Postgres migration v2', time: '2026-07-04 14:05', type: 'db' },
    { user: 'Nikshitha', action: 'Registered agent workflow scheduler', time: '2026-07-04 13:18', type: 'agent' },
    { user: 'System', action: 'Auto-purged expired vector cache nodes', time: '2026-07-04 00:00', type: 'system' }
  ];

  return (
    <div className="space-y-6 w-full pb-8">
      <PageHeader
        title="Admin Control Panel"
        subtitle="Manage contributors, connected sources, system health, and audit history"
      />

      {/* Tabs Navigation */}
      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

      <div className="mt-6">

        {/* === USERS & ROLES TAB === */}
        {activeTab === 'users' && (
          <div className="space-y-4" role="region" aria-label="Users and roles">
            <div className="flex justify-between items-center">
              <h2 className="text-sm font-semibold text-ui-text-primary">Workspace Members</h2>
              <Button
                variant="primary"
                size="sm"
                onClick={() => addToast({ message: 'Invite Member', description: 'Member invitation flow coming soon.', variant: 'info' })}
                aria-label="Invite a new team member"
              >
                Invite Member
              </Button>
            </div>
            {loading ? (
              <Loading message="Loading contributors..." />
            ) : error ? (
              <EmptyState
                title="Failed to Load Members"
                description={error}
                action={
                  <Button variant="primary" size="sm" onClick={fetchAdminData}>
                    Retry
                  </Button>
                }
              />
            ) : (
              <Table
                headers={userTableHeaders}
                data={contributors}
                renderRow={renderUserRow}
                totalPages={1}
                emptyMessage="No contributors found. Invite team members to get started."
              />
            )}
          </div>
        )}

        {/* === CONNECTED SOURCES TAB === */}
        {activeTab === 'sources' && (
          <div className="space-y-4" role="region" aria-label="Connected data sources">
            <div className="flex justify-between items-center">
              <h2 className="text-sm font-semibold text-ui-text-primary">Data Source Connections</h2>
              <Button
                variant="primary"
                size="sm"
                onClick={() => addToast({ message: 'Add Source', description: 'New connector integration coming soon.', variant: 'info' })}
              >
                Add New Source
              </Button>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {connectedSources.map((source, idx) => (
                <Card key={idx} className="p-5 border border-ui-border bg-ui-surface/40 flex flex-col gap-3" role="article" aria-label={`${source.name} - ${source.status}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl" aria-hidden="true">{source.icon}</span>
                      <div>
                        <h3 className="text-xs font-bold text-ui-text-primary">{source.name}</h3>
                        <p className="text-[10px] text-ui-text-tertiary">Sync: {source.syncFreq}</p>
                      </div>
                    </div>
                    <StatusIndicator
                      status={source.status === 'connected' ? 'active' : 'inactive'}
                      label={source.status === 'connected' ? 'Active' : 'Off'}
                    />
                  </div>
                  <Divider />
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] text-ui-text-tertiary">
                      Last sync: <time>{source.lastSync}</time>
                    </span>
                    <Button
                      variant={source.status === 'connected' ? 'ghost' : 'outline'}
                      size="sm"
                      onClick={() => addToast({
                        message: source.status === 'connected' ? 'Configure Source' : 'Connect Source',
                        description: `${source.name} configuration coming soon.`,
                        variant: 'info'
                      })}
                      aria-label={`${source.status === 'connected' ? 'Configure' : 'Connect'} ${source.name}`}
                    >
                      {source.status === 'connected' ? 'Configure' : 'Connect'}
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* === SYSTEM HEALTH TAB === */}
        {activeTab === 'health' && (
          <div className="space-y-6" role="region" aria-label="System health metrics">
            <h2 className="text-sm font-semibold text-ui-text-primary">System Resource Usage</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {systemHealthMetrics.map((metric, idx) => (
                <Card key={idx} className="p-5 border border-ui-border bg-ui-surface/40 space-y-3">
                  <div className="flex justify-between items-center">
                    <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">{metric.name}</h3>
                    <Badge variant={metric.level} size="sm">{metric.value}</Badge>
                  </div>
                  <div
                    className="w-full bg-ui-bg rounded-full h-2 border border-ui-border overflow-hidden"
                    role="progressbar"
                    aria-valuenow={metric.bar}
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-label={`${metric.name}: ${metric.value}`}
                  >
                    <div
                      className={`h-full rounded-full transition-all duration-700 ${metric.level === 'success' ? 'bg-ui-success-solid' : 'bg-ui-warning-solid'}`}
                      style={{ width: `${metric.bar}%` }}
                    />
                  </div>
                  <p className="text-[10px] text-ui-text-tertiary">
                    {metric.bar < 50 ? 'Operating normally – no action required.' : 'Moderate load detected – monitor closely.'}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* === AUDIT LOGS TAB === */}
        {activeTab === 'logs' && (
          <div className="space-y-4" role="region" aria-label="Audit logs">
            <h2 className="text-sm font-semibold text-ui-text-primary">Recent System Events</h2>
            <div className="border border-ui-border rounded-2xl overflow-hidden bg-ui-surface/20" role="log" aria-label="System audit log">
              {auditLogs.map((log, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-4 px-6 py-4 border-b border-ui-divider last:border-0 hover:bg-ui-surfaceHover transition-colors"
                  role="article"
                >
                  <Avatar name={log.user} size="sm" />
                  <div className="flex-1 space-y-0.5">
                    <p className="text-xs font-semibold text-ui-text-primary">{log.user}</p>
                    <p className="text-xs text-ui-text-secondary">{log.action}</p>
                  </div>
                  <div className="text-right space-y-1 shrink-0">
                    <span className="text-[10px] text-ui-text-tertiary block">
                      <time>{log.time}</time>
                    </span>
                    <Badge variant={log.type === 'deploy' ? 'brand' : log.type === 'system' ? 'info' : 'secondary'} size="sm">
                      {log.type}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* === SETTINGS TAB === */}
        {activeTab === 'settings' && (
          <div className="space-y-6 max-w-2xl" role="region" aria-label="System settings">
            <h2 className="text-sm font-semibold text-ui-text-primary">System Configuration</h2>

            <Card className="p-6 border border-ui-border bg-ui-surface/40 space-y-5">
              <div>
                <label
                  htmlFor="indexing-frequency"
                  className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider block mb-3"
                >
                  Indexing Frequency
                </label>
                <select
                  id="indexing-frequency"
                  className="w-full bg-ui-bg border border-ui-border text-ui-text-primary rounded-lg text-sm px-3.5 py-2.5 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/20"
                >
                  <option className="bg-ui-surface">Every 2 hours</option>
                  <option className="bg-ui-surface">Every 4 hours</option>
                  <option className="bg-ui-surface">Every 12 hours</option>
                  <option className="bg-ui-surface">Daily</option>
                </select>
              </div>

              <Divider />

              <div>
                <label
                  htmlFor="cache-ttl"
                  className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider block mb-3"
                >
                  Vector Cache TTL (seconds)
                </label>
                <input
                  id="cache-ttl"
                  type="number"
                  defaultValue={3600}
                  min={60}
                  max={86400}
                  className="w-full bg-ui-bg border border-ui-border text-ui-text-primary rounded-lg text-sm px-3.5 py-2.5 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/20"
                />
              </div>

              <Divider />

              <div>
                <label
                  htmlFor="max-nodes"
                  className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider block mb-3"
                >
                  Max Nodes Per Graph Query
                </label>
                <input
                  id="max-nodes"
                  type="number"
                  defaultValue={500}
                  min={10}
                  max={5000}
                  className="w-full bg-ui-bg border border-ui-border text-ui-text-primary rounded-lg text-sm px-3.5 py-2.5 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/20"
                />
              </div>

              <div className="pt-2 flex justify-end gap-3">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => addToast({ message: 'Reset', description: 'Settings reset to defaults.', variant: 'info' })}
                >
                  Reset to Defaults
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  loading={savingSettings}
                  onClick={handleSaveSettings}
                >
                  Save Settings
                </Button>
              </div>
            </Card>
          </div>
        )}

      </div>
    </div>
  );
};

export default Admin;
