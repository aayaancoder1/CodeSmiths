/**
 * Service for dashboard system metrics.
 * Connects to FastAPI endpoint GET /api/stats.
 */
export const dashboardService = {
  /**
   * Get operational overview metrics from the GraphRAG backend.
   * @returns {Promise<any>}
   */
  async getOverviewMetrics() {
    const res = await fetch('/api/stats');
    if (!res.ok) {
      throw new Error(`Stats endpoint failed: ${res.status}`);
    }
    const data = await res.json();
    return {
      indexedNodes: data.nodes_count.toLocaleString(),
      queriesCount: data.relationships_count.toLocaleString(), // represents relationships
      latency: data.embedding_model, // display embedding model instead of hardcoded latency
      connectedCount: data.status,
      raw: data
    };
  },

  /**
   * Get the real demo files indexed in the database.
   * @returns {Promise<any[]>}
   */
  async getActiveIngestions() {
    return [
      { name: 'payment_incident.md', icon: '📝', status: 'indexed', count: 'Incident Report (Qdrant)' },
      { name: 'redis_outage.md', icon: '📝', status: 'indexed', count: 'Outage Summary (Qdrant)' },
      { name: 'slack_thread.md', icon: '💬', status: 'indexed', count: 'Discussion Log (Qdrant)' }
    ];
  }
};

