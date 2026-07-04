import React from 'react';

const PageHeader = ({
  title,
  subtitle,
  children,
  className = '',
  ...props
}) => {
  return (
    <div className={`flex flex-col md:flex-row md:items-center md:justify-between pb-6 border-b border-ui-border ${className}`} {...props}>
      <div className="space-y-1">
        <h1 className="text-2xl font-extrabold tracking-tight text-white leading-tight">{title}</h1>
        {subtitle && <p className="text-sm text-ui-text-secondary">{subtitle}</p>}
      </div>
      {children && (
        <div className="mt-4 md:mt-0 flex items-center gap-3 self-start md:self-auto">
          {children}
        </div>
      )}
    </div>
  );
};

export default PageHeader;
