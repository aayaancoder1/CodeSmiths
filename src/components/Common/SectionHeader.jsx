import React from 'react';

const SectionHeader = ({ title, description, children, className = '' }) => {
  return (
    <div className={`flex items-center justify-between py-4 ${className}`}>
      <div>
        <h3 className="text-lg font-medium leading-6 text-slate-100">{title}</h3>
        {description && <p className="mt-1 text-sm text-slate-400">{description}</p>}
      </div>
      {children && <div className="flex items-center gap-2">{children}</div>}
    </div>
  );
};

export default SectionHeader;
