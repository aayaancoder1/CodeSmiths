import React from 'react';
import PageContainer from '../../components/Common/PageContainer';
import PageHeader from '../../components/Common/PageHeader';
import Table from '../../components/Tables/Table';
import Button from '../../components/Buttons/Button';

const Admin = () => {
  const mockUsers = [
    { id: 1, name: 'Thanmayee', role: 'Frontend Owner', status: 'Active' },
    { id: 2, name: 'Aayaan', role: 'AI pipelines / RAG', status: 'Active' },
    { id: 3, name: 'Kishan', role: 'FastAPI / DB', status: 'Active' },
    { id: 4, name: 'Nikshitha', role: 'Agent Workflows', status: 'Active' }
  ];

  return (
    <PageContainer>
      <PageHeader 
        title="Admin Settings" 
        subtitle="Manage users, system configurations, and permission contracts"
      />

      <div className="space-y-6">
        <h3 className="text-lg font-semibold text-white">Workspace Contributors</h3>
        <Table headers={['ID', 'Name', 'Role', 'Status', 'Actions']}>
          {mockUsers.map((user) => (
            <tr key={user.id} className="hover:bg-slate-800/20 transition-colors">
              <td className="px-6 py-4 font-mono text-slate-400">{user.id}</td>
              <td className="px-6 py-4 text-white font-medium">{user.name}</td>
              <td className="px-6 py-4 text-slate-300">{user.role}</td>
              <td className="px-6 py-4">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400">
                  {user.status}
                </span>
              </td>
              <td className="px-6 py-4">
                <Button variant="ghost" size="sm">Edit</Button>
              </td>
            </tr>
          ))}
        </Table>
      </div>
    </PageContainer>
  );
};

export default Admin;
