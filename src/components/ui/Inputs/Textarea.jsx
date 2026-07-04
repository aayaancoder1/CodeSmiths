import React from 'react';

const Textarea = ({
  label,
  error,
  className = '',
  disabled = false,
  rows = 4,
  required = false,
  ...props
}) => {
  return (
    <div className={`space-y-1.5 w-full ${className}`}>
      {label && (
        <label className="block text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
          {label} {required && <span className="text-ui-danger-solid">*</span>}
        </label>
      )}

      <textarea
        disabled={disabled}
        rows={rows}
        className={`w-full bg-ui-bg border text-ui-text-primary rounded-lg text-sm transition-colors duration-150 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 placeholder-ui-text-tertiary disabled:opacity-50 disabled:bg-ui-surface p-3.5 ${
          error ? 'border-ui-danger-border focus:border-ui-danger-solid' : 'border-ui-border hover:border-ui-borderHover'
        }`}
        {...props}
      />

      {error && <p className="text-xs text-ui-danger-text font-medium">{error}</p>}
    </div>
  );
};

export default Textarea;
