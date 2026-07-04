import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchInput from '../../components/ui/Inputs/SearchInput';
import CitationCard from '../../components/ui/Cards/CitationCard';
import Loading from '../../components/ui/Feedback/Loading';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import PageHeader from '../../components/ui/Layout/PageHeader';
import Button from '../../components/ui/Buttons/Button';

const Search = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

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

  // Dummy mock data generator for search
  const handleSearch = (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setHasSearched(true);
    setResults([]);

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

      // Filter results
      const filtered = allResults.filter(item => {
        const matchesSource = selectedSource === 'all' || item.sourceType === selectedSource;
        const matchesConfidence = item.confidence >= minConfidence;
        const matchesQuery = item.documentTitle.toLowerCase().includes(query.toLowerCase());
        return matchesSource && matchesConfidence && matchesQuery;
      });

      setResults(filtered);
      setLoading(false);
    }, 1000);
  };

  const handleSuggestedClick = (suggested) => {
    setQuery(suggested);
    setLoading(true);
    setHasSearched(true);
    setTimeout(() => {
      setResults([
        {
          id: 1,
          documentTitle: `${suggested} Configuration & Setup Guidelines`,
          source: 'Notion Workspace / Internal-Guides',
          pageNumber: 2,
          timestamp: 'Updated 1 day ago',
          confidence: 98,
          sourceType: 'notion',
          docId: 'internal-guides'
        }
      ]);
      setLoading(false);
    }, 800);
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
          <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
            <SearchInput
              value={query}
              onChange={(val) => setQuery(val)}
              onClear={() => {
                setQuery('');
                setResults([]);
                setHasSearched(false);
              }}
              placeholder="Search documents, transcripts, and codebases..."
              className="flex-1"
            />
            <Button type="submit" variant="primary" loading={loading}>
              Search Brain
            </Button>
          </form>

          {/* Suggested prompts bubble */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-ui-text-tertiary">Try searches:</span>
            {suggestedSearches.map((sug, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSuggestedClick(sug)}
                className="text-xs px-2.5 py-1 rounded-full bg-ui-surface border border-ui-border text-ui-text-secondary hover:text-ui-text-primary hover:border-ui-borderHover transition-all focus:outline-none focus:ring-1 focus:ring-brand-500/30"
              >
                {sug}
              </button>
            ))}
          </div>

          {/* Results List */}
          <div className="pt-2">
            {loading ? (
              <Loading message="Querying organization data graph..." />
            ) : hasSearched && results.length === 0 ? (
              <EmptyState 
                title="No results found" 
                description={`No documentation or logs matched "${query}" with current filters.`}
              />
            ) : hasSearched ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs text-ui-text-tertiary">
                  <span>Found {results.length} relevant documents</span>
                  <span>Sorted by confidence matches</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {results.map((res) => (
                    <CitationCard
                      key={res.id}
                      documentTitle={res.documentTitle}
                      source={res.source}
                      pageNumber={res.pageNumber}
                      timestamp={res.timestamp}
                      confidence={res.confidence}
                      onOpen={() => navigate(`/documents/${res.docId}`)}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <EmptyState
                title="Search the corporate brain"
                description="Input a keyword, file path, or concept to trace semantic node citations."
                icon={
                  <svg className="w-12 h-12 text-ui-text-tertiary stroke-[1.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                }
              />
            )}
          </div>
        </div>

        {/* Filters & Recent Panel (1 column wide) */}
        <div className="space-y-6">
          {/* Filters Card */}
          <div className="p-5 bg-ui-surface/40 border border-ui-border rounded-2xl space-y-4">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Search Filters</h3>
            
            {/* Source Dropdown */}
            <div className="space-y-2">
              <label className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block">Source Node</label>
              <select
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
                <span>Confidence Match</span>
                <span className="text-brand-400 font-bold">{minConfidence}%+</span>
              </div>
              <input
                type="range"
                min="30"
                max="95"
                value={minConfidence}
                onChange={(e) => setMinConfidence(Number(e.target.value))}
                className="w-full h-1.5 bg-ui-bg rounded-lg appearance-none cursor-pointer accent-brand-500 border border-ui-border"
              />
            </div>
          </div>

          {/* Recent Searches */}
          <div className="p-5 bg-ui-surface/40 border border-ui-border rounded-2xl space-y-3">
            <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">Recent Searches</h3>
            <div className="space-y-2">
              {recentSearches.map((rec, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => {
                    setQuery(rec);
                    handleSuggestedClick(rec);
                  }}
                  className="w-full text-left text-xs text-ui-text-secondary hover:text-brand-400 truncate p-2 rounded-lg bg-ui-bg/50 border border-ui-border/50 hover:bg-ui-surfaceHover hover:border-ui-border transition-all focus:outline-none"
                >
                  🔍 {rec}
                </button>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Search;
