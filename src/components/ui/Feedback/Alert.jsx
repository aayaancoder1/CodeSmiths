import React, { useState } from 'react';

const Alert = ({
  title,
  children,
  variant = 'info', // 'info' | 'success' | 'warning' | 'danger'
  onClose,
  className = '',
  ...props
}) => {
  const [isOpen, setIsOpen] = useState(true);

  if (!isOpen) return null;

  const variants = {
    info: {
      container: 'bg-ui-info-bg/30 border-ui-info-border text-ui-info-text',
      icon: (
        <svg className="w-5 h-5 text-ui-info-solid flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    success: {
      container: 'bg-ui-success-bg/30 border-ui-success-border text-ui-success-text',
      icon: (
        <svg className="w-5 h-5 text-ui-success-solid flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    warning: {
      container: 'bg-ui-warning-bg/30 border-ui-warning-border text-ui-warning-text',
      icon: (
        <svg className="w-5 h-5 text-ui-warning-solid flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      ),
    },
    danger: {
      container: 'bg-ui-danger-bg/30 border-ui-danger-border text-ui-danger-text',
      icon: (
        <svg className="w-5 h-5 text-ui-danger-solid flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
  };

  const currentVariant = variants[variant] || variants.info;

  const handleClose = () => {
    setIsOpen(false);
    if (onClose) onClose();
  };

  return (
    <div
      role="alert"
      className={`flex items-start gap-3 p-4 border rounded-xl transition-all duration-150 ${currentVariant.container} ${className}`}
      {...props}
    >
      {currentVariant.icon}
      
      <div className="flex-1 space-y-1">
        {title && <h5 className="font-semibold text-sm leading-none">{title}</h5>}
        {children && <div className="text-xs opacity-90 leading-relaxed">{children}</div>}
      </div>

      {onClose && (
        <button
          type="button"
          onClick={handleClose}
          className="p-1 rounded-lg hover:bg-white/10 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-current"
          aria-label="Dismiss alert"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default Alert;
