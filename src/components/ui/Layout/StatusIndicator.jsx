import React from 'react';

const StatusIndicator = ({
  status = 'info', // 'success' | 'warning' | 'danger' | 'info' | 'neutral'
  label,
  className = '',
  ...props
}) => {
  const styles = {
    success: 'bg-ui-success-bg/15 text-ui-success-text border-ui-success-border/20',
    warning: 'bg-ui-warning-bg/15 text-ui-warning-text border-ui-warning-border/20',
    danger: 'bg-ui-danger-bg/15 text-ui-danger-text border-ui-danger-border/20',
    info: 'bg-ui-info-bg/15 text-ui-info-text border-ui-info-border/20',
    neutral: 'bg-ui-surface text-ui-text-secondary border-ui-border',
  };

  const dots = {
    success: 'bg-ui-success-solid',
    warning: 'bg-ui-warning-solid',
    danger: 'bg-ui-danger-solid',
    info: 'bg-ui-info-solid',
    neutral: 'bg-ui-text-tertiary',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold border capitalize select-none ${styles[status]} ${className}`}
      {...props}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${dots[status]}`} />
      <span>{label || status}</span>
    </span>
  );
};

export default StatusIndicator;
