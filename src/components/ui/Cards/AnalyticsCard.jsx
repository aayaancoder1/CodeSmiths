import React from 'react';
import Card from './Card';

const AnalyticsCard = ({
  title,
  subtitle,
  children,
  action,
  className = '',
  ...props
}) => {
  return (
    <Card className={`relative flex flex-col ${className}`} {...props}>
      {(title || subtitle || action) && (
        <div className="flex items-center justify-between pb-4 border-b border-ui-divider mb-4">
          <div>
            {title && <h4 className="text-sm font-bold text-white tracking-wide">{title}</h4>}
            {subtitle && <p className="text-xs text-ui-text-tertiary mt-0.5">{subtitle}</p>}
          </div>
          {action && <div className="text-xs">{action}</div>}
        </div>
      )}
      
      {/* Content body wrapper */}
      <div className="flex-1 w-full relative">
        {children}
      </div>
    </Card>
  );
};

export default AnalyticsCard;
