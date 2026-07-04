import React from 'react';

const EmptyState = ({ title, description, icon = '📭', children, className = '' }) => {
  return (
    <div className={`flex flex-col items-center justify-center text-center p-8 rounded-2xl border border-dashed border-slate-800 bg-slate-900/50 ${className}`}>
      <span className="text-4xl mb-4 select-none">{icon}</span>
      <h3 className="text-base font-semibold text-slate-200">{title}</h3>
      {description && <p className="mt-1 text-sm text-slate-500 max-w-sm">{description}</p>}
      {children && <div className="mt-6">{children}</div>}
    </div>
  );
};

export default EmptyState;
