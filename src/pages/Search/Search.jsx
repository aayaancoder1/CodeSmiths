import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchInput from '../../components/ui/Inputs/SearchInput';
import CitationCard from '../../components/ui/Cards/CitationCard';
import Loading from '../../components/ui/Feedback/Loading';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import PageHeader from '../../components/ui/Layout/PageHeader';
import Button from '../../components/ui/Buttons/Button';
import { useToast } from '../../context/ToastContext';

/**
 * Search page — performs semantic search across connected knowledge sources.
 * Wired to service layer: replace the mock resolver with searchService.query()
 * when the backend endpoint is available.
 */
const Search = () => {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState(null);

  // Filters
  const [selectedSource, setSelectedSource] = useState('all');
  const [minConfidence, setMinConfidence] = useState(60);

  const recentSearches = [
    'AWS security keys configuration',
    'employee policy manual Q2 2026',
    'react context performance recommendations'
  ];

  const suggestedSearches = [
    'Ingestion pipelines configuration',
    'SSO setup guide',
    'Frontend roadmap'
  ];

  const sourceOptions = [
    { value: 'all', label: 'All Sources' },
    { value: 'drive', label: 'Google Drive' },
    { value: 'notion', label: 'Notion Workspace' },
    { value: 'slack', label: 'Slack Channels' },
    { value: 'github', label: 'GitHub Repository' }
  ];

  /**
   * resolveSearchResults — placeholder resolver using mock data.
   * Replace with: `await searchService.query(query, { source: selectedSource, minConfidence })`
   * when backend is ready.
   */
  const resolveSearchResults = async (searchQuery, source, confidence) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const allResults = [
          {
            id: 1,
            documentTitle: 'AWS Security Best Practices & IAM Roles',
            source: 'Google Drive / security-policy-v4.pdf',
            pageNumber: 12,
            timestamp: 'Updated 2 days ago',
            confidence: 94,
            sourceType: 'drive',
            docId: 'security-policy-v4'
          },
          {
            id: 2,
            documentTitle: 'SSO Login Integration Guide & SSO Token Renewal',
            source: 'Notion Workspace / Engineering / Auth.md',
            pageNumber: 3,
            timestamp: 'Updated 1 week ago',
            confidence: 86,
            sourceType: 'notion',
            docId: 'sso-login-guide'
          },
          {
            id: 3,
            documentTitle: 'Frontend State Management & React Guidelines',
            source: 'GitHub / codesmiths-core / docs / state.md',
            pageNumber: 1,
            timestamp: 'Updated 3 mins ago',
            confidence: 72,
            sourceType: 'github',
            docId: 'state-management'
          },
          {
            id: 4,
            documentTitle: 'Production Deployment Ingestion Log Output',
            source: 'Slack Channels / #ops-deployment-feed',
            pageNumber: null,
            timestamp: 'Updated 4 hours ago',
            confidence: 58,
            sourceType: 'slack',
            docId: 'production-deployment'
          }
        ];

        const filtered = allResults.filter((item) => {
          const matchesSource = source === 'all' || item.sourceType === source;
          const matchesConfidence = item.confidence >= confidence;
          const matchesQuery =
            !searchQuery ||
            item.documentTitle.toLowerCase().includes(searchQuery.toLowerCase());
          return matchesSource && matchesConfidence && matchesQuery;
        });

        resolve(filtered);
      }, 1000);
    });
  };

  const handleSearch = async (e, overrideQuery) => {
    if (e) e.preventDefault();
    const activeQuery = overrideQuery !== undefined ? overrideQuery : query;
    if (!activeQuery.trim()) return;

    setLoading(true);
    setHasSearched(true);
    setResults([]);
    setError(null);

    try {
      const data = await resolveSearchResults(activeQuery, selectedSource, minConfidence);
      setResults(data);
      if (data.length === 0) {
        addToast({
          message: 'No results found',
          description: `No documents matched "${activeQuery}" with current filters.`,
          variant: 'info'
        });
      }
    } catch (err) {
      console.error('Search error:', err);
      setError('Search failed. Please try again.');
      addToast({
        message: 'Search Failed',
        description: 'An error occurred while querying the knowledge graph.',
        variant: 'danger'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestedClick = async (suggested) => {
    setQuery(suggested);
    await handleSearch(null, suggested);
  };

  const clearSearch = () => {
    setQuery('');
    setResults([]);
    setHasSearched(false);
    setError(null);
  };

  return (
    <div className="space-y-6 w-full pb-8">
      <PageHeader
        title="Knowledge Search"
        subtitle="Perform semantic searches across Slack, Notion, GitHub and internal drives"
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">

        {/* Search & Results Panel (3 columns wide) */}
        <div className="lg:col-span-3 space-y-6">
          <form
            onSubmit={handleSearch}
            className="flex flex-col sm:flex-row gap-3"
            role="search"
            aria-label="Knowledge base search"
          >
            <label htmlFor="search-input" className="sr-only">Search the knowledge base</label>
            <SearchInput
              id="search-input"
              value={query}
              onChange={(val) => setQuery(val)}
              onClear={clearSearch}
              placeholder="Search documents, transcripts, and codebases..."
              className="flex-1"
            />
            <Button
              type="submit"
              variant="primary"
              loading={loading}
              disabled={!query.trim()}
              aria-label="Execute search"
            >
              Search Brain
            </Button>
          </form>

          {/* Suggested prompts bubble */}
          <div className="flex flex-wrap items-center gap-2" aria-label="Suggested searches">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-ui-text-tertiary">
              Try searches:
            </span>
            {suggestedSearches.map((sug, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSuggestedClick(sug)}
                disabled={loading}
                className="text-xs px-2.5 py-1 rounded-full bg-ui-surface border border-ui-border text-ui-text-secondary hover:text-ui-text-primary hover:border-ui-borderHover transition-all focus:outline-none focus-visible:ring-1 focus-visible:ring-brand-500/30 disabled:opacity-50"
                aria-label={`Search for: ${sug}`}
              >
                {sug}
              </button>
            ))}
          </div>

          {/* Results List */}
          <div className="pt-2" aria-live="polite" aria-atomic="false">
            {loading ? (
              <Loading message="Querying organization data graph..." />
            ) : error ? (
              <EmptyState
                title="Search Error"
                description={error}
                action={
                  <Button variant="primary" size="sm" onClick={() => handleSearch(null, query)}>
                    Retry Search
                  </Button>
                }
              />
            ) : hasSearched && results.length === 0 ? (
              <EmptyState
                title="No results found"
                description={`No documentation or logs matched "${query}" with current filters. Try adjusting the filters or searching with different keywords.`}
              />
            ) : hasSearched ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs text-ui-text-tertiary">
                  <span>Found <strong className="text-ui-text-secondary">{results.length}</strong> relevant documents</span>
                  <span>Sorted by confidence match</span>
                </div>
                <div
                  className="grid grid-cols-1 sm:grid-cols-2 gap-4"
                  role="list"
                  aria-label={`${results.length} search results`}
                >
                  {results.map((res) => (
                    <div key={res.id} role="listitem">
                      <CitationCard
                        documentTitle={res.documentTitle}
                        source={res.source}
                        pageNumber={res.pageNumber}
                        timestamp={res.timestamp}
                        confidence={res.confidence}
                        onOpen={() => navigate(`/documents/${res.docId}`)}
                      />
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <EmptyState
                title="Search the corporate brain"
                description="Input a keyword, file path, or concept to trace semantic node citations."
                icon={
                  <svg className="w-12 h-12 text-ui-text-tertiary stroke-[1.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                }
              />
            )}
          </div>
        </div>

        {/* Filters & Recent Panel (1 column wide) */}
        <aside className="space-y-6" aria-label="Search filters and recent searches">
          {/* Filters Card */}
          <div className="p-5 bg-ui-surface/40 border border-ui-border rounded-2xl space-y-4">
            <h2 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
              Search Filters
            </h2>

            {/* Source Dropdown */}
            <div className="space-y-2">
              <label
                htmlFor="source-filter"
                className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block"
              >
                Source Node
              </label>
              <select
                id="source-filter"
                value={selectedSource}
                onChange={(e) => setSelectedSource(e.target.value)}
                className="w-full bg-ui-bg border border-ui-border text-ui-text-primary rounded-lg text-sm px-3.5 py-2.5 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/20"
              >
                {sourceOptions.map((opt) => (
                  <option key={opt.value} value={opt.value} className="bg-ui-surface">
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Slider / Confidence Filter */}
            <div className="space-y-2">
              <div className="flex justify-between items-center text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider">
                <label htmlFor="confidence-filter">Confidence Match</label>
                <span className="text-brand-400 font-bold" aria-live="polite">{minConfidence}%+</span>
              </div>
              <input
                id="confidence-filter"
                type="range"
                min="30"
                max="95"
                value={minConfidence}
                onChange={(e) => setMinConfidence(Number(e.target.value))}
                className="w-full h-1.5 bg-ui-bg rounded-lg appearance-none cursor-pointer accent-brand-500 border border-ui-border"
                aria-label={`Minimum confidence: ${minConfidence}%`}
              />
            </div>
          </div>

          {/* Recent Searches */}
          <div className="p-5 bg-ui-surface/40 border border-ui-border rounded-2xl space-y-3">
            <h2 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
              Recent Searches
            </h2>
            <div className="space-y-2" role="list" aria-label="Recent search history">
              {recentSearches.map((rec, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSuggestedClick(rec)}
                  disabled={loading}
                  className="w-full text-left text-xs text-ui-text-secondary hover:text-brand-400 truncate p-2 rounded-lg bg-ui-bg/50 border border-ui-border/50 hover:bg-ui-surfaceHover hover:border-ui-border transition-all focus:outline-none focus-visible:ring-1 focus-visible:ring-brand-500/30 disabled:opacity-50"
                  role="listitem"
                  aria-label={`Repeat search: ${rec}`}
                >
                  <span aria-hidden="true">🔍 </span>{rec}
                </button>
              ))}
            </div>
          </div>
        </aside>

      </div>
    </div>
  );
};

export default Search;
