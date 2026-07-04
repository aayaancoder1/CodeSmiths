/**
 * Service for Knowledge Graph queries and visualizations.
 */
export const graphService = {
  /**
   * Fetch nodes and edges data representing topology.
   * @param {string} [filter]
   * @returns {Promise<{nodes: any[], edges: any[]}>}
   */
  async getTopology(filter) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const nodes = [
          { id: 'n1', label: 'AWS Config', type: 'service', x: 150, y: 150 },
          { id: 'n2', label: 'OAuth Gateway', type: 'gateway', x: 300, y: 120 },
          { id: 'n3', label: 'Auth.md', type: 'document', x: 220, y: 240 },
          { id: 'n4', label: 'IAM Roles Spec', type: 'document', x: 400, y: 220 },
          { id: 'n5', label: 'Ingestion Pipeline', type: 'process', x: 100, y: 300 }
        ];

        const edges = [
          { from: 'n1', to: 'n2', label: 'secures' },
          { from: 'n3', to: 'n2', label: 'documents' },
          { from: 'n4', to: 'n1', label: 'defines' },
          { from: 'n5', to: 'n3', label: 'indexes' }
        ];

        if (filter) {
          const lower = filter.toLowerCase();
          const filteredNodes = nodes.filter(n => n.label.toLowerCase().includes(lower) || n.type.toLowerCase().includes(lower));
          const nodeIds = new Set(filteredNodes.map(n => n.id));
          const filteredEdges = edges.filter(e => nodeIds.has(e.from) && nodeIds.has(e.to));
          resolve({ nodes: filteredNodes, edges: filteredEdges });
        } else {
          resolve({ nodes, edges });
        }
      }, 400);
    });
  },

  /**
   * Get metadata properties for a specific entity node.
   * @param {string} nodeId
   * @returns {Promise<any>}
   */
  async getNodeMetadata(nodeId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const metadata = {
          n1: { id: 'n1', title: 'AWS Config Node', type: 'Service Endpoint', details: 'Coordinates IAM credentials verification checks.', lastModified: '10m ago' },
          n2: { id: 'n2', title: 'OAuth Gateway Node', type: 'Gateway Process', details: 'Validates JWT access tokens for external consumer requests.', lastModified: '3h ago' },
          n3: { id: 'n3', title: 'Auth.md Document', type: 'Reference Document', details: 'Contains setup guides and token endpoints for onboarding developer roles.', lastModified: '1d ago' },
          n4: { id: 'n4', title: 'IAM Roles Spec Document', type: 'Reference Document', details: 'Outlines the security posture mapping credentials to specific clusters.', lastModified: '4d ago' },
          n5: { id: 'n5', title: 'Ingestion Pipeline Process', type: 'Ingest Process', details: 'Monitors Notion, Slack and GitHub commits every 2 hours.', lastModified: 'Just now' }
        };
        resolve(metadata[nodeId] || null);
      }, 250);
    });
  }
};
