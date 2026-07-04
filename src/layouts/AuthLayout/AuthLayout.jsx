import React from 'react';
import { Outlet } from 'react-router-dom';

const AuthLayout = ({ className = '' }) => {
  return (
    <div className={`min-h-screen flex items-center justify-center bg-slate-950 px-4 py-12 sm:px-6 lg:px-8 ${className}`}>
      <div className="max-w-md w-full space-y-8 bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">
        <Outlet />
      </div>
    </div>
  );
};

export default AuthLayout;
