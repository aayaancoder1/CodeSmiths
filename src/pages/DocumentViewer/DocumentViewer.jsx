import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '../../components/ui/Buttons/Button';
import Badge from '../../components/ui/Feedback/Badge';
import Card from '../../components/ui/Cards/Card';
import Loading from '../../components/ui/Feedback/Loading';
import Skeleton from '../../components/ui/Feedback/Skeleton';
import Divider from '../../components/ui/Layout/Divider';
import StatusIndicator from '../../components/ui/Layout/StatusIndicator';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import { documentService } from '../../services/documentService';
import { useToast } from '../../context/ToastContext';

const DocumentViewer = () => {
  const { documentId } = useParams();
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDoc = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await documentService.getDocumentDetails(documentId);
      if (!data) throw new Error('Document not found');
      setDoc(data);
    } catch (err) {
      console.error('Error fetching document:', err);
      setError(err.message || 'Failed to load document.');
      addToast({
        message: 'Document Error',
        description: 'Could not load the requested document from the knowledge index.',
        variant: 'danger'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDoc();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentId]);

  const handleShare = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href).then(() => {
        addToast({ message: 'Link Copied', description: 'Document link copied to clipboard.', variant: 'success' });
      });
    } else {
      addToast({ message: 'Share', description: 'Copy the URL from your browser to share.', variant: 'info' });
    }
  };

  const handleDownload = () => {
    addToast({ message: 'Download Started', description: 'Document download will begin shortly.', variant: 'info' });
  };

  // Skeleton for document loading
  if (loading) {
    return (
      <div className="space-y-6 w-full pb-8">
        {/* Header skeleton */}
        <div className="flex flex-col sm:flex-row items-start justify-between gap-4">
          <div className="space-y-2">
            <Skeleton variant="text" className="w-32 h-3" aria-hidden="true" />
            <Skeleton variant="text" className="w-80 h-7" aria-hidden="true" />
            <Skeleton variant="text" className="w-24 h-4 mt-1" aria-hidden="true" />
          </div>
          <div className="flex gap-2">
            <Skeleton variant="rect" className="w-28 h-8 rounded-lg" aria-hidden="true" />
            <Skeleton variant="rect" className="w-24 h-8 rounded-lg" aria-hidden="true" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-3 space-y-4">
            <Skeleton variant="rect" className="h-64 rounded-2xl" aria-hidden="true" />
            <div className="space-y-2 mt-4">
              <Skeleton variant="text" className="w-32 h-3" aria-hidden="true" />
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Skeleton variant="rect" className="h-20 rounded-xl" aria-hidden="true" />
                <Skeleton variant="rect" className="h-20 rounded-xl" aria-hidden="true" />
              </div>
            </div>
          </div>
          <Skeleton variant="rect" className="h-64 rounded-2xl" aria-hidden="true" />
        </div>

        <div className="py-8">
          <Loading message="Loading document from knowledge index..." />
        </div>
      </div>
    );
  }

  if (error || !doc) {
    return (
      <div className="py-16">
        <EmptyState
          title="Document Not Found"
          description={error || `The document "${documentId}" could not be found in the knowledge index.`}
          action={
            <div className="flex gap-3">
              <Button variant="outline" size="sm" onClick={() => navigate('/search')}>
                ← Back to Search
              </Button>
              <Button variant="primary" size="sm" onClick={fetchDoc}>
                Retry
              </Button>
            </div>
          }
        />
      </div>
    );
  }

  return (
    <div className="space-y-6 w-full pb-8">
      {/* Document Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <nav className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider text-ui-text-tertiary" aria-label="Breadcrumb">
            <button
              onClick={() => navigate('/search')}
              className="hover:text-brand-400 transition-colors focus:outline-none focus-visible:ring-1 focus-visible:ring-brand-500/50 rounded"
              aria-label="Go back to search"
            >
              ← Back to Search
            </button>
            <span aria-hidden="true">/ Document Viewer</span>
          </nav>
          <h1 className="text-xl font-extrabold tracking-tight text-white leading-snug">{doc.title}</h1>
          <div className="flex flex-wrap items-center gap-2 mt-1">
            <Badge variant="info" size="sm">Knowledge Index</Badge>
            <StatusIndicator status="active" label="Indexed" />
          </div>
        </div>

        <div className="flex gap-2 shrink-0">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleShare}
            aria-label="Share document link"
          >
            Share Document
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleDownload}
            aria-label="Download document"
          >
            <span aria-hidden="true">⬇ </span>Download
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">

        {/* Main Content Area */}
        <main className="lg:col-span-3 space-y-6">
          {/* Document Body */}
          <Card className="border border-ui-border bg-ui-surface/40 overflow-hidden">
            {/* Content Header */}
            <div className="px-8 py-5 border-b border-ui-divider bg-ui-bg/30 flex justify-between items-center">
              <div className="flex items-center gap-2 text-xs text-ui-text-secondary">
                <span aria-hidden="true">📄</span>
                <span className="font-medium">{doc.source}</span>
              </div>
              <Badge variant="secondary" size="sm">Page 1 of 12</Badge>
            </div>

            {/* Scrollable body */}
            <article className="p-8 max-h-[420px] overflow-y-auto space-y-4" aria-label="Document content">
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                {doc.content}
              </p>
              <Divider />
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                All engineers with access to AWS resources are required to adhere to the{' '}
                <mark className="bg-brand-500/20 text-brand-300 px-1 py-0.5 rounded font-medium">
                  Principle of Least Privilege
                </mark>{' '}
                at all times. This applies to IAM roles, S3 bucket policies, and Lambda function execution roles.
              </p>
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                Section 3.2: API token rotation schedules must be enforced automatically using the{' '}
                <mark className="bg-amber-500/20 text-amber-300 px-1 py-0.5 rounded font-medium">
                  codesmiths-token-rotator
                </mark>{' '}
                utility. Manual overrides must be logged to the audit trail within the Admin Control Panel.
              </p>
              <p className="text-sm text-ui-text-secondary leading-relaxed">
                Section 4.1: VPC isolation policies must prevent any cross-account resource sharing unless
                explicitly allowlisted through the enterprise Security Review Board process. All exception
                requests require written sign-off from the CISO.
              </p>
            </article>
          </Card>

          {/* Related Documents Section */}
          <section className="space-y-3" aria-label="Related knowledge nodes">
            <h2 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
              Related Knowledge Nodes
            </h2>
            {doc.relatedDocs && doc.relatedDocs.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {doc.relatedDocs.map((related, idx) => (
                  <button
                    key={idx}
                    onClick={() => navigate(`/documents/${related.id}`)}
                    className="p-4 text-left border border-ui-border bg-ui-surface/40 hover:bg-ui-surfaceHover hover:border-ui-borderHover rounded-xl transition-all group focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50"
                    aria-label={`Open related document: ${related.title}`}
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-lg text-ui-text-tertiary group-hover:text-brand-400 transition-colors" aria-hidden="true">📄</span>
                      <div>
                        <h3 className="text-xs font-bold text-ui-text-primary group-hover:text-brand-300 transition-colors">
                          {related.title}
                        </h3>
                        <p className="text-[10px] text-ui-text-tertiary mt-0.5">View related document →</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <EmptyState
                title="No related documents"
                description="No related knowledge nodes are linked to this document."
              />
            )}
          </section>
        </main>

        {/* Sidebar Metadata Panel */}
        <aside className="space-y-4" aria-label="Document metadata">
          <Card className="p-5 border border-ui-border bg-ui-surface/40 space-y-4">
            <h2 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
              Document Metadata
            </h2>

            <dl className="space-y-3 text-xs">
              <div className="space-y-0.5">
                <dt className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider">Document ID</dt>
                <dd>
                  <code className="text-ui-text-primary font-mono text-[11px] bg-ui-bg px-2 py-1 rounded border border-ui-border block">
                    {doc.id}
                  </code>
                </dd>
              </div>

              <Divider />

              <div className="space-y-0.5">
                <dt className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider">Created By</dt>
                <dd className="text-ui-text-secondary">{doc.creator}</dd>
              </div>

              <div className="space-y-0.5">
                <dt className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider">File Size</dt>
                <dd className="text-ui-text-secondary">{doc.fileSize}</dd>
              </div>

              <div className="space-y-0.5">
                <dt className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider">Indexed At</dt>
                <dd className="text-ui-text-secondary">
                  <time>{doc.createdTime}</time>
                </dd>
              </div>

              <Divider />

              <div className="space-y-0.5">
                <dt className="text-[10px] uppercase font-semibold text-ui-text-tertiary tracking-wider">Source Connector</dt>
                <dd className="text-ui-text-secondary truncate" title={doc.source}>{doc.source}</dd>
              </div>
            </dl>
          </Card>
        </aside>

      </div>
    </div>
  );
};

export default DocumentViewer;
