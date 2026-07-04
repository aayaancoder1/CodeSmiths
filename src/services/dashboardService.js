/**
 * Service for dashboard system metrics.
 */
export const dashboardService = {
  /**
   * Get operational overview metrics.
   * @returns {Promise<any>}
   */
  async getOverviewMetrics() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          indexedNodes: '84,290',
          queriesCount: '1,842',
          latency: '108ms',
          connectedCount: '4 / 6'
        });
      }, 300);
    });
  },

  /**
   * Get active ingestion run status details.
   * @returns {Promise<any[]>}
   */
  async getActiveIngestions() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { name: 'Google Drive', icon: '📂', status: 'connected', count: '1,420 docs' },
          { name: 'Notion Workspace', icon: '📝', status: 'connected', count: '458 pages' },
          { name: 'Slack Channels', icon: '💬', status: 'connected', count: '12 channels' },
          { name: 'GitHub Codebase', icon: '💻', status: 'connected', count: '8 repos' }
        ]);
      }, 400);
    });
  }
};
