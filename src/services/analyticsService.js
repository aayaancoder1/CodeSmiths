/**
 * Service placeholder for handling system telemetry analytics.
 */
export const analyticsService = {
  /**
   * Fetch aggregate storage and query rate telemetries.
   * @param {string} range - e.g. '7d', '30d'
   * @returns {Promise<any>}
   */
  async getTelemetryStats(range) {
    // Placeholder method - No implementation.
    return Promise.resolve(null);
  },

  /**
   * Fetch system node latency aggregates.
   * @returns {Promise<any>}
   */
  async getLatencyStats() {
    // Placeholder method - No implementation.
    return Promise.resolve(null);
  }
};
