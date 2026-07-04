import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '../../components/ui/Buttons/Button';
import Badge from '../../components/ui/Feedback/Badge';
import Card from '../../components/ui/Cards/Card';
import Loading from '../../components/ui/Feedback/Loading';
import Divider from '../../components/ui/Layout/Divider';
import StatusIndicator from '../../components/ui/Layout/StatusIndicator';
import { documentService } from '../../services/documentService';

const DocumentViewer = () => {
  const { documentId } = useParams();
  const navigate = useNavigate();
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDoc = async () => {
      try {
        const data = await documentService.getDocumentDetails(documentId);
        setDoc(data);
      } catch (err) {
        console.error('Error fetching document:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDoc();
  }, [documentId]);

  if (loading) {
    return (
      <div className="py-24">
        <Loading message="Loading document from knowledge index..." />
      </div>
    );
  }

  if (!doc) {
    return (
      <div className="py-16 text-center text-ui-text-tertiary text-sm">
        Document not found in index.
      </div>
    );
  }

  return (
    <div className="space-y-6 w-full pb-8">
      {/* Document Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider text-ui-text-tertiary">
            <button
              onClick={() => navigate('/search')}
              className="hover:text-brand-400 transition-colors focus:outline-none"
            >
              ← Back to Search
            </button>
            <span>/ Document Viewer</span>
          </div>
          <h1 className="text-xl font-extrabold tracking-tight text-white leading-snug">{doc.title}</h1>
          <div className="flex flex-wrap items-center gap-2 mt-1">
            <Badge variant="info" size="sm">Knowledge Index</Badge>
            <StatusIndicator status="active" label="Indexed" />
          </div>
        </div>

        <div className="flex gap-2 shrink-0">
          <Button variant="secondary" size="sm">
            Share Document
          </Button>
          <Button variant="outline" size="sm">
            ⬇ Download
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        
        {/* Main Content Area */}
        <div className="lg:col-span-3 space-y-6">
          {/* Document Body */}
          <Card className="border border-ui-border bg-ui-surface/40 overflow-hidden">
            {/* Content Header */}
            <div className="px-8 py-5 border-b border-ui-divider bg-ui-bg/30 flex justify-between items-center">
              <div className="flex items-center gap-2 text-xs text-ui-text-secondary">
                <span>📄</span>
                <span className="font-medium">{doc.source}</span>
              </div>
              <Badge variant="secondary" size="sm">Page 1 of 12</Badge>
            </div>

            {/* Scrollable body */}
            <div className="p-8 max-h-[420px] overflow-y-auto space-y-4">
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                {doc.content}
              </p>
              <Divider />
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                All engineers with access to AWS resources are required to adhere to the{' '}
                <span className="bg-brand-500/20 text-brand-300 px-1 py-0.5 rounded font-medium">
                  Principle of Least Privilege
                </span>{' '}
                at all times. This applies to IAM roles, S3 bucket policies, and Lambda function execution roles.
              </p>
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                Section 3.2: API token rotation schedules must be enforced automatically using the{' '}
                <span className="bg-amber-500/20 text-amber-300 px-1 py-0.5 rounded font-medium">
                  codesmiths-token-rotator
                </span>{' '}
                utility. Manual overrides must be logged to the audit trail within the Admin Control Panel.
              </p>
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                Section 4.1: VPC isolation policies must prevent any cross-account resource sharing unless explicitly allowlisted through the enterprise Security Review Board process. All exception requests require written sign-off from the CISO.
              </p>
            </div>
          </Card>

          {/* Related Documents Section */}
          <div className="space-y-3">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Related Knowledge Nodes</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {doc.relatedDocs?.map((related, idx) => (
                <button
                  key={idx}
                  onClick={() => navigate(`/documents/${related.id}`)}
                  className="p-4 text-left border border-ui-border bg-ui-surface/40 hover:bg-ui-surfaceHover hover:border-ui-borderHover rounded-xl transition-all group focus:outline-none focus:ring-2 focus:ring-brand-500/20"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-lg text-ui-text-tertiary group-hover:text-brand-400 transition-colors">📄</span>
                    <div>
                      <h4 className="text-xs font-bold text-ui-text-primary group-hover:text-brand-300 transition-colors">{related.title}</h4>
                      <p className="text-[10px] text-ui-text-tertiary mt-0.5">View related document →</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar Metadata Panel */}
        <div className="space-y-4">
          <Card className="p-5 border border-ui-border bg-ui-surface/40 space-y-4">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Document Metadata</h3>
            
            <div className="space-y-3 text-xs">
              <div className="space-y-0.5">
                <span className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider block">Document ID</span>
                <code className="text-ui-text-primary font-mono text-[11px] bg-ui-bg px-2 py-1 rounded border border-ui-border block">{doc.id}</code>
              </div>

              <Divider />

              <div className="space-y-0.5">
                <span className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider block">Created By</span>
                <p className="text-ui-text-secondary">{doc.creator}</p>
              </div>

              <div className="space-y-0.5">
                <span className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider block">File Size</span>
                <p className="text-ui-text-secondary">{doc.fileSize}</p>
              </div>

              <div className="space-y-0.5">
                <span className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider block">Indexed At</span>
                <p className="text-ui-text-secondary">{doc.createdTime}</p>
              </div>

              <Divider />

              <div className="space-y-0.5">
                <span className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider block">Source Connector</span>
                <p className="text-ui-text-secondary truncate">{doc.source}</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default DocumentViewer;
