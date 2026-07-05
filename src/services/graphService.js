/**
 * Service for Knowledge Graph queries and visualizations.
 * Connected to FastAPI endpoint GET /api/graph.
 */

// Cache nodes for metadata queries
let cachedNodes = [];

export const graphService = {
  /**
   * Fetch live nodes and edges from Neo4j and assign coordinates for the canvas.
   * @param {string} [filter]
   * @returns {Promise<{nodes: any[], edges: any[]}>}
   */
  async getTopology(filter) {
    const res = await fetch('/api/graph');
    if (!res.ok) {
      throw new Error(`Graph API returned error: ${res.status}`);
    }
    const data = await res.json();

    // Map visual positions (2D layout) based on node types
    const layoutMap = {
      service: { x: 150, y: 150 },
      incident: { x: 300, y: 220 },
      document: { x: 450, y: 300 }
    };

    // Keep track of counts per type for offset positioning
    const typeCounts = {};

    const nodes = data.nodes.map((node) => {
      const type = node.type.toLowerCase();
      if (!typeCounts[type]) typeCounts[type] = 0;
      typeCounts[type]++;

      // Assign position with slight spacing offset
      const basePos = layoutMap[type] || { x: 300, y: 300 };
      const offsetX = typeCounts[type] * 80 - 80;
      const offsetY = typeCounts[type] * 40 - 40;

      return {
        id: node.id,
        label: node.label,
        type: node.type,
        x: basePos.x + offsetX,
        y: basePos.y + offsetY,
        properties: node.properties
      };
    });

    cachedNodes = nodes;

    const edges = data.edges.map((edge) => ({
      from: edge.source,
      to: edge.target,
      label: edge.type
    }));

    if (filter) {
      const lower = filter.toLowerCase();
      const filteredNodes = nodes.filter(n => n.id.toLowerCase().includes(lower) || n.type.toLowerCase().includes(lower));
      const nodeIds = new Set(filteredNodes.map(n => n.id));
      const filteredEdges = edges.filter(e => nodeIds.has(e.from) && nodeIds.has(e.to));
      return { nodes: filteredNodes, edges: filteredEdges };
    }

    return { nodes, edges };
  },

  /**
   * Get metadata properties for a specific entity node from the local cache.
   * @param {string} nodeId
   * @returns {Promise<any>}
   */
  async getNodeMetadata(nodeId) {
    const node = cachedNodes.find(n => n.id === nodeId);
    if (!node) return null;

    // Convert raw properties to inspector display structure
    let detailsStr = '';
    if (node.properties) {
      detailsStr = Object.entries(node.properties)
        .map(([k, v]) => `${k}: ${v}`)
        .join('\n');
    }

    return {
      id: node.id,
      title: node.id,
      type: node.type.toUpperCase(),
      details: detailsStr || 'No details available.',
      lastModified: node.properties.timestamp || 'Synced'
    };
  }
};

