/**
 * Service for document viewer node references.
 */
export const documentService = {
  /**
   * Fetch file data and citation context by document ID.
   * @param {string} documentId
   * @returns {Promise<any>}
   */
  async getDocumentDetails(documentId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          id: documentId,
          title: documentId === 'security-policy-v4' ? 'AWS Security Best Practices & IAM Roles' : 'SSO Login Integration Guide & SSO Token Renewal',
          source: documentId === 'security-policy-v4' ? 'Google Drive / security-policy-v4.pdf' : 'Notion Workspace / Engineering / Auth.md',
          creator: 'Security Ops Team',
          fileSize: '2.4 MB',
          createdTime: '2026-03-12 14:02:18',
          content: 'This document defines the strict requirements for AWS security and Identity Access Management (IAM) across all enterprise microservices. It is essential that all configuration follows standard OAuth2 flows and rotates API tokens every 30 days. Failure to rotate credentials will trigger automatic service suspensions in the operations monitoring hub.',
          relatedDocs: [
            { id: 'aws-microservices-config', title: 'AWS Microservices Configuration Guide' },
            { id: 'oauth2-specification', title: 'OAuth2 Authentication Flow Spec' }
          ]
        });
      }, 400);
    });
  }
};
