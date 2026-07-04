import React from 'react';
import { Outlet } from 'react-router-dom';

const AuthLayout = ({ className = '' }) => {
  return (
    <div className={`min-h-screen flex items-center justify-center bg-ui-bg px-4 py-12 sm:px-6 lg:px-8 ${className}`}>
      {/* Subtle background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f2433_1px,transparent_1px),linear-gradient(to_bottom,#1f2433_1px,transparent_1px)] bg-[size:32px_32px] opacity-30 pointer-events-none" />
      <div className="relative z-10 max-w-md w-full">
        <Outlet />
      </div>
    </div>
  );
};

export default AuthLayout;
