/**
 * Service for handling Chat and QA model interactions.
 * Connects to the FastAPI GraphRAG backend via POST /api/ask.
 */

const API_BASE = '/api';

export const chatService = {
  /**
   * Send a query message to the GraphRAG pipeline.
   * @param {string} sessionId
   * @param {string} query
   * @returns {Promise<any>}
   */
  async sendMessage(sessionId, query) {
    const response = await fetch(`${API_BASE}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server error: ${response.status}`);
    }

    const data = await response.json();
    return {
      raw: data,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sender: 'assistant'
    };
  },

  /**
   * Fetch chat history logs for a session.
   * @param {string} sessionId
   * @returns {Promise<any[]>}
   */
  async getHistory(sessionId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: 1,
            sender: 'assistant',
            text: 'Hello! I am your AI Enterprise Assistant powered by GraphRAG. Ask me any question about company incidents, services, or documents.',
            time: '10:00 AM'
          }
        ]);
      }, 400);
    });
  }
};
