import React from 'react';
import PageContainer from '../../components/Common/PageContainer';
import PageHeader from '../../components/Common/PageHeader';
import Input from '../../components/Inputs/Input';
import Button from '../../components/Buttons/Button';
import Card from '../../components/Cards/Card';

const Search = () => {
  return (
    <PageContainer>
      <PageHeader 
        title="Search UI" 
        subtitle="Full text and vector semantic search engine query tool"
      />
      
      <div className="flex gap-3 max-w-2xl">
        <Input 
          placeholder="Search for nodes, files, sources, or citations..." 
          className="flex-1"
        />
        <Button variant="primary">Search</Button>
      </div>

      <div className="space-y-4 mt-6">
        <Card title="Search Results (Dummy Output)">
          <p className="text-sm text-slate-500">Perform a search query above to see matches and context mappings.</p>
        </Card>
      </div>
    </PageContainer>
  );
};

export default Search;
