import React from 'react';

const SectionHeader = ({
  title,
  description,
  children,
  className = '',
  ...props
}) => {
  return (
    <div className={`flex items-center justify-between py-4 ${className}`} {...props}>
      <div className="space-y-0.5">
        <h3 className="text-base font-bold text-slate-100">{title}</h3>
        {description && <p className="text-xs text-ui-text-tertiary">{description}</p>}
      </div>
      {children && <div className="flex items-center gap-2">{children}</div>}
    </div>
  );
};

export default SectionHeader;
