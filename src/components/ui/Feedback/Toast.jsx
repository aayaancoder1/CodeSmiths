import React from 'react';

const Toast = ({
  message,
  description,
  variant = 'info', // 'info' | 'success' | 'warning' | 'danger'
  onClose,
  className = '',
  ...props
}) => {
  const variants = {
    info: {
      border: 'border-ui-info-border/50',
      icon: (
        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-ui-info-bg/30 text-ui-info-solid">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </span>
      ),
    },
    success: {
      border: 'border-ui-success-border/50',
      icon: (
        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-ui-success-bg/30 text-ui-success-solid">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
          </svg>
        </span>
      ),
    },
    warning: {
      border: 'border-ui-warning-border/50',
      icon: (
        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-ui-warning-bg/30 text-ui-warning-solid">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </span>
      ),
    },
    danger: {
      border: 'border-ui-danger-border/50',
      icon: (
        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-ui-danger-bg/30 text-ui-danger-solid">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </span>
      ),
    },
  };

  const currentVariant = variants[variant] || variants.info;

  return (
    <div
      className={`flex items-start gap-3 p-4 bg-ui-surface/90 backdrop-blur-md border rounded-xl shadow-2xl max-w-sm w-full animate-slide-in pointer-events-auto ${currentVariant.border} ${className}`}
      {...props}
    >
      {currentVariant.icon}
      <div className="flex-1 space-y-1">
        <h5 className="font-semibold text-sm text-ui-text-primary leading-tight">{message}</h5>
        {description && <p className="text-xs text-ui-text-secondary leading-normal">{description}</p>}
      </div>
      {onClose && (
        <button
          type="button"
          onClick={onClose}
          className="text-ui-text-tertiary hover:text-ui-text-primary p-0.5 rounded-lg hover:bg-ui-surface transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50"
          aria-label="Close message"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default Toast;
