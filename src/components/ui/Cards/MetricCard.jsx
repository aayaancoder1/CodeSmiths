import React from 'react';
import Card from './Card';

const MetricCard = ({
  title,
  value,
  change,
  changeType = 'positive', // 'positive' | 'negative' | 'neutral'
  icon,
  className = '',
  ...props
}) => {
  const trendColor = {
    positive: 'text-ui-success-text bg-ui-success-bg/20 border-ui-success-border/30',
    negative: 'text-ui-danger-text bg-ui-danger-bg/20 border-ui-danger-border/30',
    neutral: 'text-ui-text-tertiary bg-ui-surface/50 border-ui-border',
  };

  const trendIcon = {
    positive: '↑',
    negative: '↓',
    neutral: '→',
  };

  return (
    <Card className={`relative overflow-hidden ${className}`} {...props}>
      <div className="flex justify-between items-start">
        <span className="text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">{title}</span>
        {icon && <span className="text-lg opacity-70 select-none">{icon}</span>}
      </div>

      <div className="mt-4 flex items-baseline justify-between">
        <span className="text-3xl font-extrabold tracking-tight text-white">{value}</span>
        {change && (
          <span className={`inline-flex items-center gap-1 text-xs font-bold px-2 py-0.5 rounded-full border ${trendColor[changeType]}`}>
            <span>{trendIcon[changeType]}</span>
            <span>{change}</span>
          </span>
        )}
      </div>
    </Card>
  );
};

export default MetricCard;
