import React, { useState, useEffect, useRef } from 'react';
import PageHeader from '../../components/ui/Layout/PageHeader';
import Card from '../../components/ui/Cards/Card';
import Button from '../../components/ui/Buttons/Button';
import SearchInput from '../../components/ui/Inputs/SearchInput';
import Loading from '../../components/ui/Feedback/Loading';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import Badge from '../../components/ui/Feedback/Badge';
import { graphService } from '../../services/graphService';
import { useToast } from '../../context/ToastContext';

const KnowledgeGraph = () => {
  const { addToast } = useToast();
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNode, setSelectedNode] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);
  const [nodeDetails, setNodeDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [hoveredNode, setHoveredNode] = useState(null);

  // Pan and Zoom States
  const [pan, setPan] = useState({ x: 100, y: 100 });
  const [zoom, setZoom] = useState(1);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const svgRef = useRef(null);

  useEffect(() => {
    fetchGraphData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchQuery]);

  const fetchGraphData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await graphService.getTopology(searchQuery);
      setNodes(data.nodes);
      setEdges(data.edges);
      
      // Auto-center or fit to screen if nodes exist
      if (data.nodes.length > 0) {
        setPan({ x: 150, y: 100 });
      }
    } catch (err) {
      console.error('Error loading topology:', err);
      setError('Failed to load live database topology.');
    } finally {
      setLoading(false);
    }
  };

  const handleNodeClick = async (node, e) => {
    if (e) e.stopPropagation();
    setSelectedEdge(null);
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

  const handleEdgeClick = (edge, e) => {
    if (e) e.stopPropagation();
    setSelectedNode(null);
    setNodeDetails(null);
    setSelectedEdge(edge);
  };

  const zoomIn = () => setZoom((z) => Math.min(z + 0.15, 2.5));
  const zoomOut = () => setZoom((z) => Math.max(z - 0.15, 0.4));
  const resetView = () => {
    setZoom(1);
    setPan({ x: 100, y: 100 });
    setSelectedNode(null);
    setSelectedEdge(null);
    setNodeDetails(null);
  };

  const handleMouseDown = (e) => {
    // Only drag on canvas background
    if (e.target.tagName === 'svg' || e.target.id === 'bg-grid' || e.target.id === 'canvas-group') {
      setIsDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const getNodeColor = (type, isSelected) => {
    if (isSelected) return '#f59e0b'; // Gold selected status

    switch (type?.toLowerCase()) {
      case 'service': return '#10b981'; // Green
      case 'incident': return '#ef4444'; // Red
      case 'document': return '#3b82f6'; // Blue
      case 'slack thread':
      case 'ticket': return '#8b5cf6'; // Purple
      default: return '#6b7280';
    }
  };

  const getStats = () => {
    const counts = { service: 0, incident: 0, document: 0, thread: 0, other: 0 };
    nodes.forEach(n => {
      const type = n.type?.toLowerCase();
      if (type === 'service') counts.service++;
      else if (type === 'incident') counts.incident++;
      else if (type === 'document') counts.document++;
      else if (type === 'slack thread' || type === 'ticket') counts.thread++;
      else counts.other++;
    });
    return counts;
  };

  const stats = getStats();

  return (
    <div className="space-y-4 w-full pb-6 select-none relative">
      <PageHeader
        title="Knowledge Graph Explorer"
        subtitle="Live visualization of indexed nodes and relationships stored inside Neo4j"
      />

      <div className="flex flex-col lg:flex-row gap-4 h-[70vh] min-h-[580px] w-full">
        {/* Main Canvas Area (90% width or left panel) */}
        <div className="flex-1 border border-ui-border bg-ui-bg/75 rounded-2xl relative overflow-hidden flex flex-col shadow-2xl">
          {/* Controls HUD */}
          <div className="absolute top-4 left-4 z-10 flex flex-wrap gap-2 items-center">
            <SearchInput
              value={searchQuery}
              onChange={(val) => setSearchQuery(val)}
              onClear={() => setSearchQuery('')}
              placeholder="Search nodes or types..."
              className="w-52 md:w-60 bg-ui-surface/85 backdrop-blur-md"
            />
            <Button variant="outline" size="sm" onClick={fetchGraphData} className="bg-ui-surface/85 backdrop-blur-md">
              ↻ Refresh
            </Button>
          </div>

          <div className="absolute top-4 right-4 z-10 flex gap-1 bg-ui-surface/85 backdrop-blur-md p-1 border border-ui-border rounded-xl shadow-lg">
            <button onClick={zoomIn} className="px-2.5 py-1 text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-all" title="Zoom In">+</button>
            <button onClick={zoomOut} className="px-2.5 py-1 text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-all" title="Zoom Out">-</button>
            <button onClick={resetView} className="px-2.5 py-1 text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition-all">Reset</button>
          </div>

          {/* SVG Canvas */}
          <div
            className="flex-grow w-full h-full cursor-grab active:cursor-grabbing outline-none"
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            {loading ? (
              <div className="absolute inset-0 flex items-center justify-center bg-ui-bg/60 backdrop-blur-xs z-20">
                <Loading message="Fetching live Neo4j database graph..." />
              </div>
            ) : error ? (
              <div className="absolute inset-0 flex items-center justify-center z-20">
                <EmptyState title="Graph Query Failed" description={error} />
              </div>
            ) : nodes.length === 0 ? (
              <div className="absolute inset-0 flex items-center justify-center z-20">
                <EmptyState title="No nodes found matching filters" description="Try querying different tags." />
              </div>
            ) : (
              <svg
                ref={svgRef}
                className="w-full h-full"
                onClick={() => {
                  setSelectedNode(null);
                  setSelectedEdge(null);
                  setNodeDetails(null);
                }}
              >
                <defs>
                  <pattern id="graph-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#171b26" strokeWidth="0.8" />
                  </pattern>
                  {/* Arrow marker for relations */}
                  <marker
                    id="arrow"
                    viewBox="0 0 10 10"
                    refX="26"
                    refY="5"
                    markerWidth="6"
                    markerHeight="6"
                    orient="auto-start-reverse"
                  >
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155" />
                  </marker>
                  <marker
                    id="arrow-selected"
                    viewBox="0 0 10 10"
                    refX="26"
                    refY="5"
                    markerWidth="6"
                    markerHeight="6"
                    orient="auto-start-reverse"
                  >
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b" />
                  </marker>
                </defs>
                <rect width="100%" height="100%" fill="url(#graph-grid)" id="bg-grid" />

                {/* Main transform group */}
                <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`} id="canvas-group">
                  {/* Edges layer */}
                  {edges.map((edge, idx) => {
                    const fromNode = nodes.find(n => n.id === edge.from);
                    const toNode = nodes.find(n => n.id === edge.to);
                    if (!fromNode || !toNode) return null;

                    const isSelected = selectedEdge === edge;
                    const isHighlighted = hoveredNode?.id === edge.from || hoveredNode?.id === edge.to;

                    const midX = (fromNode.x + toNode.x) / 2;
                    const midY = (fromNode.y + toNode.y) / 2;

                    return (
                      <g key={idx} className="cursor-pointer" onClick={(e) => handleEdgeClick(edge, e)}>
                        <line
                          x1={fromNode.x}
                          y1={fromNode.y}
                          x2={toNode.x}
                          y2={toNode.y}
                          stroke={isSelected ? '#f59e0b' : isHighlighted ? '#94a3b8' : '#272d3d'}
                          strokeWidth={isSelected ? 3.5 : isHighlighted ? 2.5 : 1.8}
                          markerEnd={`url(#${isSelected ? 'arrow-selected' : 'arrow'})`}
                          className="transition-all"
                        />
                        {/* Interactive invisible hover line for easier clicking */}
                        <line
                          x1={fromNode.x}
                          y1={fromNode.y}
                          x2={toNode.x}
                          y2={toNode.y}
                          stroke="transparent"
                          strokeWidth={12}
                        />
                        <text
                          x={midX}
                          y={midY - 6}
                          fill={isSelected ? '#f59e0b' : '#64748b'}
                          fontSize="9"
                          fontWeight={isSelected ? 'bold' : 'normal'}
                          textAnchor="middle"
                          className="font-mono bg-ui-bg select-none"
                        >
                          {edge.label}
                        </text>
                      </g>
                    );
                  })}

                  {/* Nodes layer */}
                  {nodes.map((node) => {
                    const isSelected = selectedNode?.id === node.id;
                    const isHovered = hoveredNode?.id === node.id;
                    const nodeColor = getNodeColor(node.type, isSelected);

                    return (
                      <g
                        key={node.id}
                        transform={`translate(${node.x}, ${node.y})`}
                        onClick={(e) => handleNodeClick(node, e)}
                        onMouseEnter={() => setHoveredNode(node)}
                        onMouseLeave={() => setHoveredNode(null)}
                        className="cursor-pointer select-none"
                      >
                        {/* Pulse effect */}
                        {isSelected && (
                          <circle r="22" fill="none" stroke="#f59e0b" strokeWidth="2" className="animate-ping opacity-60" />
                        )}
                        <circle
                          r={isHovered ? 18 : 15}
                          fill={nodeColor}
                          stroke={isSelected ? '#ffffff' : '#090a0f'}
                          strokeWidth="2"
                          className="transition-all shadow-lg"
                        />
                        <text
                          y="32"
                          fill={isSelected ? '#f59e0b' : '#ffffff'}
                          fontSize="10"
                          fontWeight="bold"
                          textAnchor="middle"
                          className="drop-shadow-md"
                        >
                          {node.label}
                        </text>
                        <text
                          y="-22"
                          fill="#64748b"
                          fontSize="8"
                          fontWeight="bold"
                          textAnchor="middle"
                          className="uppercase tracking-wider opacity-85"
                        >
                          {node.type}
                        </text>
                      </g>
                    );
                  })}
                </g>
              </svg>
            )}
          </div>

          {/* Stats HUD (Bottom Left) */}
          <div className="absolute bottom-4 left-4 z-10 bg-ui-surface/85 backdrop-blur-md p-3.5 border border-ui-border rounded-2xl shadow-xl space-y-2 text-[10px] text-ui-text-secondary w-48 pointer-events-none">
            <h4 className="font-extrabold text-white uppercase tracking-wider text-[9px] border-b border-ui-divider pb-1">Graph Statistics</h4>
            <div className="grid grid-cols-2 gap-1.5 font-bold">
              <div>Nodes: <span className="text-white">{nodes.length}</span></div>
              <div>Edges: <span className="text-white">{edges.length}</span></div>
              <div className="col-span-2 pt-1 border-t border-ui-divider grid grid-cols-2 gap-1">
                <span className="text-emerald-400">🟢 Services: {stats.service}</span>
                <span className="text-red-400">🔴 Incidents: {stats.incident}</span>
                <span className="text-blue-400">🔵 Documents: {stats.document}</span>
                <span className="text-purple-400">🟣 Chat Logs: {stats.thread}</span>
              </div>
            </div>
          </div>

          {/* Legend HUD (Bottom Right) */}
          <div className="absolute bottom-4 right-4 z-10 bg-ui-surface/85 backdrop-blur-md p-3 border border-ui-border rounded-xl shadow-xl text-[10px] text-ui-text-secondary flex gap-3 flex-wrap">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[#10b981]" /> Service</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[#ef4444]" /> Incident</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[#3b82f6]" /> Document</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[#8b5cf6]" /> Chat/Thread</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[#f59e0b]" /> Selected</span>
          </div>
        </div>

        {/* HUD inspector panel (Right 300px side panel) */}
        <div className="w-full lg:w-72 bg-ui-surface/40 border border-ui-border rounded-2xl p-5 flex flex-col justify-between shadow-2xl backdrop-blur-md">
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-ui-divider pb-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-brand-500" /> HUD Inspector
            </h3>

            {selectedNode && (
              <div className="space-y-4 text-xs animate-fade-in">
                <div>
                  <span className="text-[9px] uppercase font-bold text-ui-text-tertiary tracking-widest block mb-1">Node Type</span>
                  <Badge variant="brand" size="sm">{selectedNode.type?.toUpperCase()}</Badge>
                </div>
                <div>
                  <span className="text-[9px] uppercase font-bold text-ui-text-tertiary tracking-widest block mb-1">Entity ID</span>
                  <h4 className="font-extrabold text-white leading-tight break-all">{selectedNode.id}</h4>
                </div>
                {detailsLoading ? (
                  <div className="py-4"><Loading message="Loading database context..." /></div>
                ) : nodeDetails ? (
                  <div>
                    <span className="text-[9px] uppercase font-bold text-ui-text-tertiary tracking-widest block mb-1">Database Properties</span>
                    <pre className="p-3 bg-ui-bg/70 border border-ui-border rounded-xl font-mono text-[10px] text-ui-text-secondary leading-normal whitespace-pre-wrap max-h-56 overflow-y-auto">
                      {nodeDetails.details}
                    </pre>
                  </div>
                ) : null}
              </div>
            )}

            {selectedEdge && (
              <div className="space-y-4 text-xs animate-fade-in">
                <div>
                  <span className="text-[9px] uppercase font-bold text-ui-text-tertiary tracking-widest block mb-1">Relationship Type</span>
                  <Badge variant="warning" size="sm">{selectedEdge.label}</Badge>
                </div>
                <div className="space-y-2 bg-ui-bg/70 p-3 rounded-xl border border-ui-border font-mono text-[10px] text-ui-text-secondary">
                  <div>Source Node: <br /><strong className="text-white">{selectedEdge.from}</strong></div>
                  <div className="pt-2 border-t border-ui-divider">Target Node: <br /><strong className="text-white">{selectedEdge.to}</strong></div>
                </div>
              </div>
            )}

            {!selectedNode && !selectedEdge && (
              <div className="text-center py-24 text-xs text-ui-text-tertiary leading-relaxed">
                🔍 Click on any entity node or directed edge in the viewport to inspect its properties.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeGraph;
