import React from 'react';
import PageContainer from '../../components/Common/PageContainer';
import PageHeader from '../../components/Common/PageHeader';
import Graph from '../../components/Graph/Graph';

const KnowledgeGraph = () => {
  return (
    <PageContainer>
      <PageHeader 
        title="Knowledge Graph" 
        subtitle="Visual representation of entity relationships and connections"
      />
      
      {/* Graph Visual Panel */}
      <Graph />
    </PageContainer>
  );
};

export default KnowledgeGraph;
