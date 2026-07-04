import React from 'react';
import PageContainer from '../../components/Common/PageContainer';
import PageHeader from '../../components/Common/PageHeader';
import Chart from '../../components/Charts/Chart';
import Card from '../../components/Cards/Card';

const Analytics = () => {
  return (
    <PageContainer>
      <PageHeader 
        title="Analytics Dashboard" 
        subtitle="Detailed operational telemetry, storage reports, and usage rates"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card title="Total Storage Saved" value="1.2 TB" change="+45 GB" changeType="positive" icon="💾" />
        <Card title="Queries Answered" value="284,912" change="+12,401" changeType="positive" icon="✔️" />
        <Card title="Active Integrations" value="14" change="0" changeType="positive" icon="🔌" />
        <Card title="Database Health" value="99.9%" change="Optimal" changeType="positive" icon="❤️" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <Chart title="Storage Ingestion History" type="bar" />
        <Chart title="API Endpoint Latencies" type="line" />
      </div>
    </PageContainer>
  );
};

export default Analytics;
