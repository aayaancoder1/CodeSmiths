/**
 * Service for handling Chat and QA model interactions.
 */
export const chatService = {
  /**
   * Send a query message to the agent retrieval stream.
   * @param {string} sessionId
   * @param {string} query
   * @returns {Promise<any>}
   */
  async sendMessage(sessionId, query) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          text: `Here is what I found regarding "${query}". Based on Notion page "SSO Integration Guide" (page 2) and Google Drive file "security-policy-v4.pdf", you can find detailed setup checklists with 94% relevance. Would you like me to extract the steps for you?`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          sender: 'assistant'
        });
      }, 1000);
    });
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
            text: 'Hello! I am your AI Enterprise Assistant. Ask me any question related to indexed drives, Notion docs, Slack messages, or GitHub logs.',
            time: '10:00 AM'
          }
        ]);
      }, 400);
    });
  }
};
