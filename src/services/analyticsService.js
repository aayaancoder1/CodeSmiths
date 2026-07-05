/**
 * Service for handling system telemetry analytics.
 */
export const analyticsService = {
  /**
   * Fetch aggregate storage and query rate telemetries.
   * @param {string} range - e.g. '7d', '30d'
   * @returns {Promise<any>}
   */
  async getTelemetryStats(range = '7d') {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          storageSaved: '1.2 TB',
          queriesCount: '284,912',
          activeIntegrations: '14',
          dbHealth: '99.9%'
        });
      }, 300);
    });
  },

  /**
   * Fetch system node latency aggregates.
   * @returns {Promise<any>}
   */
  async getLatencyStats() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          avgLatency: '142ms',
          p95Latency: '210ms',
          p99Latency: '320ms'
        });
      }, 250);
    });
  }
};
