import React from 'react';

const Badge = ({
  children,
  variant = 'brand', // 'brand' | 'success' | 'warning' | 'danger' | 'info' | 'secondary'
  size = 'md', // 'sm' | 'md'
  className = '',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-full select-none';

  const variants = {
    brand: 'bg-brand-500/10 text-brand-400 border border-brand-500/20',
    success: 'bg-ui-success-bg text-ui-success-text border border-ui-success-border/30',
    warning: 'bg-ui-warning-bg text-ui-warning-text border border-ui-warning-border/30',
    danger: 'bg-ui-danger-bg text-ui-danger-text border border-ui-danger-border/30',
    info: 'bg-ui-info-bg text-ui-info-text border border-ui-info-border/30',
    secondary: 'bg-ui-surface text-ui-text-secondary border border-ui-border',
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-[10px] tracking-wide',
    md: 'px-2.5 py-1 text-xs',
  };

  return (
    <span
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
};

export default Badge;
