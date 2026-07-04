import React from 'react';
import Breadcrumb from '../Common/Breadcrumb';

const TopNavbar = ({ className = '' }) => {
  return (
    <header className={`h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6 shrink-0 ${className}`}>
      {/* Left side: Breadcrumb / Page context */}
      <div className="flex items-center space-x-4">
        <Breadcrumb />
      </div>

      {/* Right side: User Profile Placeholder / Status */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-3">
          <div className="text-right hidden sm:block">
            <p className="text-xs font-semibold text-slate-200">Thanmayee</p>
            <p className="text-[10px] text-slate-500">Frontend Lead</p>
          </div>
          <div className="w-9 h-9 rounded-full bg-brand-500 border border-slate-700 flex items-center justify-center font-bold text-sm text-white shadow-md">
            TM
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopNavbar;
