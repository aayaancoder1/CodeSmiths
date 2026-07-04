import React from 'react';
import { useParams, Link } from 'react-router-dom';
import PageContainer from '../../components/Common/PageContainer';
import PageHeader from '../../components/Common/PageHeader';
import Button from '../../components/Buttons/Button';

const DocumentViewer = () => {
  const { documentId } = useParams();

  return (
    <PageContainer>
      <PageHeader 
        title={`Document Viewer`} 
        subtitle={`Reviewing node reference metadata`}
      >
        <Link to="/search">
          <Button variant="secondary">Back to Search</Button>
        </Link>
      </PageHeader>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-6">
        <div>
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Document Resource ID</h4>
          <p className="mt-1 text-lg font-mono text-white font-semibold">{documentId}</p>
        </div>

        <div className="border-t border-slate-800 pt-6 space-y-4">
          <h4 className="text-sm font-semibold text-slate-200">Source Content Placeholder</h4>
          <p className="text-sm text-slate-400 leading-relaxed max-w-3xl">
            This is an enterprise document viewer placeholder. The backend/AI retrieval layer will ingest reference source texts, PDF raw data or graph node properties, mapping them here for visual verification.
          </p>
        </div>
      </div>
    </PageContainer>
  );
};

export default DocumentViewer;
