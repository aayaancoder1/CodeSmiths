import React from 'react';

const PageHeader = ({ title, subtitle, children, className = '' }) => {
  return (
    <div className={`flex flex-col sm:flex-row sm:items-center sm:justify-between pb-6 border-b border-slate-800/60 ${className}`}>
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight text-white">{title}</h1>
        {subtitle && <p className="text-sm text-slate-400">{subtitle}</p>}
      </div>
      {children && <div className="mt-4 sm:mt-0 flex items-center gap-3">{children}</div>}
    </div>
  );
};

export default PageHeader;
