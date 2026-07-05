import React, { useState } from 'react';

const Input = ({
  label,
  type = 'text',
  error,
  icon,
  className = '',
  disabled = false,
  required = false,
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false);

  const isPassword = type === 'password';
  const inputType = isPassword && showPassword ? 'text' : type;

  return (
    <div className={`space-y-1.5 w-full ${className}`}>
      {label && (
        <label className="block text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
          {label} {required && <span className="text-ui-danger-solid">*</span>}
        </label>
      )}
      
      <div className="relative flex items-center">
        {icon && (
          <span className="absolute left-3.5 text-ui-text-tertiary select-none pointer-events-none">
            {icon}
          </span>
        )}

        <input
          type={inputType}
          disabled={disabled}
          className={`w-full bg-ui-bg border text-ui-text-primary rounded-lg text-sm transition-colors duration-150 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 placeholder-ui-text-tertiary disabled:opacity-50 disabled:bg-ui-surface ${
            icon ? 'pl-10' : 'pl-3.5'
          } ${
            isPassword ? 'pr-10' : 'pr-3.5'
          } py-2.5 ${
            error ? 'border-ui-danger-border focus:border-ui-danger-solid focus:ring-ui-danger-solid/10' : 'border-ui-border hover:border-ui-borderHover'
          }`}
          {...props}
        />

        {isPassword && !disabled && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 text-ui-text-tertiary hover:text-ui-text-secondary text-xs font-medium focus:outline-none"
          >
            {showPassword ? 'Hide' : 'Show'}
          </button>
        )}
      </div>

      {error && <p className="text-xs text-ui-danger-text font-medium">{error}</p>}
    </div>
  );
};

export default Input;
