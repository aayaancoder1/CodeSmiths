import React from 'react';

const Tag = ({
  children,
  onRemove,
  variant = 'secondary', // 'brand' | 'success' | 'warning' | 'danger' | 'info' | 'secondary'
  size = 'md', // 'sm' | 'md'
  className = '',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center gap-1.5 font-medium rounded-md select-none transition-colors';

  const variants = {
    brand: 'bg-brand-500/10 text-brand-400 border border-brand-500/20',
    success: 'bg-ui-success-bg text-ui-success-text border border-ui-success-border/30',
    warning: 'bg-ui-warning-bg text-ui-warning-text border border-ui-warning-border/30',
    danger: 'bg-ui-danger-bg text-ui-danger-text border border-ui-danger-border/30',
    info: 'bg-ui-info-bg text-ui-info-text border border-ui-info-border/30',
    secondary: 'bg-ui-surface text-ui-text-secondary border border-ui-border hover:text-ui-text-primary hover:border-ui-borderHover',
  };

  const sizes = {
    sm: 'px-1.5 py-0.5 text-[10px]',
    md: 'px-2 py-1 text-xs',
  };

  return (
    <span
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      <span>{children}</span>
      {onRemove && (
        <button
          type="button"
          onClick={onRemove}
          className="p-0.5 rounded-sm hover:bg-white/10 hover:text-current transition-colors focus:outline-none focus-visible:ring-1 focus-visible:ring-current"
          aria-label="Remove tag"
        >
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </span>
  );
};

export default Tag;
