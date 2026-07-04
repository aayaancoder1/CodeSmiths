import React, { useState, useEffect } from 'react';
import PageHeader from '../../components/ui/Layout/PageHeader';
import Card from '../../components/ui/Cards/Card';
import Button from '../../components/ui/Buttons/Button';
import SearchInput from '../../components/ui/Inputs/SearchInput';
import Loading from '../../components/ui/Feedback/Loading';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import Badge from '../../components/ui/Feedback/Badge';
import { graphService } from '../../services/graphService';

const KnowledgeGraph = () => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNode, setSelectedNode] = useState(null);
  const [nodeDetails, setNodeDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);

  // Pan and Zoom States
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  useEffect(() => {
    fetchGraphData();
  }, [searchQuery]);

  const fetchGraphData = async () => {
    setLoading(true);
    try {
      const data = await graphService.getTopology(searchQuery);
      setNodes(data.nodes);
      setEdges(data.edges);
      // Reset selected node if not in results
      if (selectedNode && !data.nodes.some(n => n.id === selectedNode.id)) {
        setSelectedNode(null);
        setNodeDetails(null);
      }
    } catch (err) {
      console.error('Error loading topology:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNodeClick = async (node) => {
    setSelectedNode(node);
    setDetailsLoading(true);
    try {
      const metadata = await graphService.getNodeMetadata(node.id);
      setNodeDetails(metadata);
    } catch (err) {
      console.error('Error fetching node metadata:', err);
    } finally {
      setDetailsLoading(false);
    }
  };

  // Zoom controls
  const zoomIn = () => setZoom(z => Math.min(z + 0.1, 2));
  const zoomOut = () => setZoom(z => Math.max(z - 0.1, 0.5));
  const resetView = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  // Pan controls
  const handleMouseDown = (e) => {
    // Only drag when clicking container background
    if (e.target.tagName === 'svg' || e.target.id === 'bg-grid') {
      setIsDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPan({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const getNodeColor = (type) => {
    switch (type) {
      case 'document': return '#5c7cff'; // brand blue
      case 'service': return '#10b981'; // success emerald
      case 'gateway': return '#0ea5e9'; // info sky
      case 'process': return '#f59e0b'; // warning amber
      default: return '#64748b';
    }
  };

  return (
    <div className="space-y-6 w-full pb-8 select-none">
      <PageHeader 
        title="Knowledge Graph" 
        subtitle="Visual representation of entity relationships, files, and ingestion logs"
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        
        {/* Graph Visual Canvas (3 columns wide) */}
        <div className="lg:col-span-3 space-y-4">
          <Card className="p-4 border border-ui-border bg-ui-surface/40 flex flex-col h-[550px] relative overflow-hidden">
            
            {/* Control Bar */}
            <div className="flex flex-col sm:flex-row justify-between gap-3 mb-4 z-20">
              <div className="flex items-center gap-2">
                <SearchInput
                  value={searchQuery}
                  onChange={(val) => setSearchQuery(val)}
                  onClear={() => setSearchQuery('')}
                  placeholder="Filter graph nodes..."
                  className="w-60"
                />
              </div>

              {/* Zoom Buttons */}
              <div className="flex gap-2">
                <Button variant="secondary" size="sm" onClick={zoomIn}>Zoom In (+)</Button>
                <Button variant="secondary" size="sm" onClick={zoomOut}>Zoom Out (-)</Button>
                <Button variant="ghost" size="sm" onClick={resetView}>Reset View</Button>
              </div>
            </div>

            {/* SVG Visual Canvas Area */}
            <div 
              className="flex-grow border border-ui-border bg-ui-bg/70 rounded-xl relative overflow-hidden cursor-grab active:cursor-grabbing"
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
            >
              {loading ? (
                <div className="absolute inset-0 flex items-center justify-center bg-ui-bg/50 backdrop-blur-sm z-10">
                  <Loading message="Rendering network connections..." />
                </div>
              ) : nodes.length === 0 ? (
                <div className="absolute inset-0 flex items-center justify-center z-10">
                  <EmptyState 
                    title="No Nodes Match Query" 
                    description="Try searching with other tags like 'auth', 'roles' or 'pipeline'." 
                  />
                </div>
              ) : (
                <svg className="w-full h-full">
                  {/* Grid Pattern background */}
                  <defs>
                    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
                      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1f2433" strokeWidth="0.5" />
                    </pattern>
                  </defs>
                  <rect width="100%" height="100%" fill="url(#grid)" id="bg-grid" />

                  {/* Transformed content group (Pan & Zoom) */}
                  <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
                    
                    {/* Relationship Lines (Edges) */}
                    {edges.map((edge, idx) => {
                      const fromNode = nodes.find(n => n.id === edge.from);
                      const toNode = nodes.find(n => n.id === edge.to);
                      if (!fromNode || !toNode) return null;

                      // Calculate midpoint for label
                      const midX = (fromNode.x + toNode.x) / 2;
                      const midY = (fromNode.y + toNode.y) / 2;

                      return (
                        <g key={idx}>
                          <line
                            x1={fromNode.x}
                            y1={fromNode.y}
                            x2={toNode.x}
                            y2={toNode.y}
                            stroke="#1f2433"
                            strokeWidth="2"
                            strokeDasharray="4 4"
                          />
                          <text
                            x={midX}
                            y={midY - 5}
                            fill="#64748b"
                            fontSize="8"
                            textAnchor="middle"
                            className="bg-ui-bg"
                          >
                            {edge.label}
                          </text>
                        </g>
                      );
                    })}

                    {/* Nodes Group */}
                    {nodes.map((node) => {
                      const isSelected = selectedNode?.id === node.id;
                      const nodeColor = getNodeColor(node.type);

                      return (
                        <g 
                          key={node.id} 
                          transform={`translate(${node.x}, ${node.y})`}
                          onClick={() => handleNodeClick(node)}
                          className="cursor-pointer"
                        >
                          {/* Highlight ring */}
                          {isSelected && (
                            <circle r="22" fill="none" stroke="#5c7cff" strokeWidth="2.5" className="animate-ping opacity-75" />
                          )}
                          <circle 
                            r="16" 
                            fill={nodeColor} 
                            stroke={isSelected ? '#f8fafc' : '#1f2433'} 
                            strokeWidth="2.5"
                          />
                          <text
                            y="30"
                            fill="#f8fafc"
                            fontSize="11"
                            fontWeight="bold"
                            textAnchor="middle"
                            className="pointer-events-none select-none drop-shadow-md"
                          >
                            {node.label}
                          </text>
                          <text
                            y="-24"
                            fill="#94a3b8"
                            fontSize="8"
                            textAnchor="middle"
                            className="pointer-events-none select-none opacity-80"
                          >
                            {node.type.toUpperCase()}
                          </text>
                        </g>
                      );
                    })}
                  </g>
                </svg>
              )}
            </div>

            {/* Legend Panel */}
            <div className="mt-3 pt-3 border-t border-ui-divider flex gap-4 flex-wrap text-xs text-ui-text-secondary">
              <span className="font-semibold text-ui-text-tertiary">LEGEND:</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#5c7cff]" /> Document Reference</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#10b981]" /> Service Endpoint</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#0ea5e9]" /> Gateway Router</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#f59e0b]" /> Ingestion Process</span>
            </div>
          </Card>
        </div>

        {/* Node Details Panel (1 column wide) */}
        <div className="space-y-4">
          <Card className="p-5 border border-ui-border bg-ui-surface/40 h-[550px] flex flex-col justify-between">
            <div>
              <h3 className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider mb-4">Node Inspector</h3>
              
              {detailsLoading ? (
                <div className="py-12"><Loading message="Loading metadata..." /></div>
              ) : nodeDetails ? (
                <div className="space-y-4">
                  <div className="space-y-1">
                    <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block">Entity Type</span>
                    <Badge variant="brand" size="sm">{nodeDetails.type}</Badge>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block">Title / Name</span>
                    <h4 className="text-sm font-bold text-white leading-snug">{nodeDetails.title}</h4>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block">Description Details</span>
                    <p className="text-xs text-ui-text-secondary leading-relaxed bg-ui-bg/50 p-3 rounded-lg border border-ui-border">
                      {nodeDetails.details}
                    </p>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider block">Last Synced Status</span>
                    <span className="text-xs text-ui-text-secondary">⌛ {nodeDetails.lastModified}</span>
                  </div>
                </div>
              ) : (
                <div className="text-center py-20 text-xs text-ui-text-tertiary">
                  Click a topology node to inspect its document context and sync metadata.
                </div>
              )}
            </div>

            {nodeDetails && (
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => {
                  if (nodeDetails.type.includes('Document')) {
                    window.location.href = `/documents/security-policy-v4`;
                  } else {
                    alert('This is a service node. No document viewer associated.');
                  }
                }}
                className="w-full mt-4"
              >
                Inspect Documentation
              </Button>
            )}
          </Card>
        </div>

      </div>
    </div>
  );
};

export default KnowledgeGraph;
