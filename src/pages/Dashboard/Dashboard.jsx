import React from 'react';
import PageContainer from '../../components/Common/PageContainer';
import PageHeader from '../../components/Common/PageHeader';
import Card from '../../components/Cards/Card';
import Chart from '../../components/Charts/Chart';

const Dashboard = () => {
  return (
    <PageContainer>
      <PageHeader 
        title="Dashboard" 
        subtitle="Operational overview and system metrics"
      />
      
      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="Total Retained Nodes" value="12,480" change="+12.3%" changeType="positive" icon="🕸️" />
        <Card title="Query Latency (Avg)" value="142ms" change="-4.1%" changeType="positive" icon="⚡" />
        <Card title="Active Ingestion Runs" value="3" change="+1" changeType="positive" icon="⚙️" />
      </div>

      {/* Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Chart title="System Ingestion Success Rate" type="bar" />
        <Chart title="User Activity & Inquiries" type="line" />
      </div>
    </PageContainer>
  );
};

export default Dashboard;
