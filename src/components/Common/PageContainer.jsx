import React from 'react';

const PageContainer = ({ children, className = '' }) => {
  return (
    <div className={`space-y-6 ${className}`}>
      {children}
    </div>
  );
};

export default PageContainer;
