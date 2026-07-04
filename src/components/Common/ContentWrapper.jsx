import React from 'react';

const ContentWrapper = ({ children, className = '' }) => {
  return (
    <div className={`bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm ${className}`}>
      {children}
    </div>
  );
};

export default ContentWrapper;
