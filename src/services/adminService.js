/**
 * Service for handling admin and workspace permissions.
 */
export const adminService = {
  /**
   * Fetch active database and git workspace contributor lists.
   * @returns {Promise<any[]>}
   */
  async getContributors() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { id: 1, name: 'Thanmayee', role: 'Frontend Owner', status: 'Active' },
          { id: 2, name: 'Aayaan', role: 'AI pipelines / RAG', status: 'Active' },
          { id: 3, name: 'Kishan', role: 'FastAPI / DB', status: 'Active' },
          { id: 4, name: 'Nikshitha', role: 'Agent Workflows', status: 'Active' }
        ]);
      }, 350);
    });
  },

  /**
   * Update workspace permissions or system settings rules.
   * @param {string|number} userId
   * @param {any} settings
   * @returns {Promise<any>}
   */
  async updateContributorPermissions(userId, settings) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ success: true, userId, updatedSettings: settings });
      }, 300);
    });
  }
};
