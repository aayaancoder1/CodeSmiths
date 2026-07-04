import React from 'react';

const Panel = ({
  children,
  header,
  footer,
  className = '',
  ...props
}) => {
  return (
    <div className={`flex flex-col bg-ui-surface border border-ui-border rounded-xl shadow-lg overflow-hidden ${className}`} {...props}>
      {header && (
        <div className="px-5 py-4 border-b border-ui-divider bg-ui-surface/40">
          {header}
        </div>
      )}

      <div className="flex-1 p-5 overflow-y-auto">
        {children}
      </div>

      {footer && (
        <div className="px-5 py-3.5 border-t border-ui-divider bg-ui-surface/20">
          {footer}
        </div>
      )}
    </div>
  );
};

export default Panel;
