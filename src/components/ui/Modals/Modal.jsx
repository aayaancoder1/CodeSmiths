import React, { useEffect } from 'react';

const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md', // 'sm' | 'md' | 'lg' | 'xl'
  className = '',
  ...props
}) => {
  // Prevent body scrolling when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-2xl',
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" {...props}>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-ui-bg/85 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Content */}
      <div
        className={`relative w-full ${sizes[size]} bg-ui-surface border border-ui-border rounded-2xl shadow-2xl z-10 overflow-hidden transform transition-all duration-200 animate-in fade-in zoom-in-95 ${className}`}
        role="dialog"
        aria-modal="true"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-ui-divider bg-ui-bg/20">
          <h3 className="text-sm font-semibold text-ui-text-primary uppercase tracking-wider">{title}</h3>
          <button
            onClick={onClose}
            className="text-ui-text-tertiary hover:text-ui-text-primary p-1.5 rounded-lg hover:bg-ui-surface transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50"
            aria-label="Close dialog"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Body */}
        <div className="p-6 text-sm text-ui-text-secondary max-h-[70vh] overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
