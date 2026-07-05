import React from 'react';

const EmptyState = ({
  title = "No data available",
  description = "There is no information to display here at the moment.",
  icon,
  action,
  className = '',
  ...props
}) => {
  return (
    <div
      className={`flex flex-col items-center justify-center text-center p-8 border border-dashed border-ui-border rounded-2xl bg-ui-surface/10 ${className}`}
      {...props}
    >
      <div className="text-ui-text-tertiary mb-3 flex items-center justify-center">
        {icon || (
          <svg className="w-12 h-12 stroke-[1.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5m6 4.125l2.25 2.25m0 0l2.25-2.25M12 13.875V9.75M3.75 7.5h16.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )}
      </div>
      <h3 className="text-sm font-semibold text-ui-text-primary mb-1">{title}</h3>
      <p className="text-xs text-ui-text-tertiary max-w-sm mb-4 leading-normal">{description}</p>
      {action && <div className="mt-1">{action}</div>}
    </div>
  );
};

export default EmptyState;
