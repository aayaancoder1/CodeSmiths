import React from 'react';

const Checkbox = ({
  label,
  checked,
  onChange,
  disabled = false,
  className = '',
  id,
  ...props
}) => {
  const checkboxId = id || `checkbox-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={`flex items-start gap-2.5 select-none ${className}`}>
      <div className="flex items-center h-5">
        <input
          id={checkboxId}
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange && onChange(e.target.checked)}
          disabled={disabled}
          className="w-4 h-4 bg-ui-bg border border-ui-border rounded text-brand-500 transition-all duration-150 focus:ring-2 focus:ring-brand-500/20 disabled:opacity-50 checked:bg-brand-500"
          {...props}
        />
      </div>
      {label && (
        <label
          htmlFor={checkboxId}
          className={`text-sm text-ui-text-secondary cursor-pointer font-medium disabled:opacity-50 select-none`}
        >
          {label}
        </label>
      )}
    </div>
  );
};

export default Checkbox;
