import React from 'react';

const Dropdown = ({
  label,
  value,
  onChange,
  options = [],
  error,
  className = '',
  disabled = false,
  ...props
}) => {
  return (
    <div className={`space-y-1.5 w-full ${className}`}>
      {label && (
        <label className="block text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
          {label}
        </label>
      )}

      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange && onChange(e.target.value)}
          disabled={disabled}
          className={`w-full bg-ui-bg border text-ui-text-primary rounded-lg text-sm transition-colors duration-150 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 disabled:opacity-50 appearance-none px-3.5 py-2.5 ${
            error ? 'border-ui-danger-border' : 'border-ui-border hover:border-ui-borderHover'
          }`}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} className="bg-ui-surface text-ui-text-primary">
              {opt.label}
            </option>
          ))}
        </select>
        
        {/* Dropdown custom SVG arrow indicator */}
        <div className="absolute inset-y-0 right-3.5 flex items-center pointer-events-none text-ui-text-tertiary">
          <svg className="h-4 w-4 fill-none stroke-current" viewBox="0 0 24 24" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      {error && <p className="text-xs text-ui-danger-text font-medium">{error}</p>}
    </div>
  );
};

export default Dropdown;
