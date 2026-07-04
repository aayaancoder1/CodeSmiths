import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/Sidebar/Sidebar';
import TopNavbar from '../../components/TopNavbar/TopNavbar';

const MainLayout = ({ className = '' }) => {
  return (
    <div className={`min-h-screen flex bg-slate-950 text-slate-100 ${className}`}>
      {/* Sidebar Component */}
      <Sidebar />

      {/* Main Content Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Navigation Component */}
        <TopNavbar />

        {/* Scrollable Content Area */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
