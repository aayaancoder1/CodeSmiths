import React from 'react';
import Card from './Card';

const CitationCard = ({
  sourceName,
  relevanceScore,
  excerpt,
  onClick,
  className = '',
  ...props
}) => {
  return (
    <Card 
      onClick={onClick}
      className={`border border-ui-border bg-ui-surface/60 hover:bg-ui-surfaceHover hover:border-ui-borderHover ${className}`}
      {...props}
    >
      <div className="flex justify-between items-center pb-2 border-b border-ui-border/60">
        <span className="font-semibold text-xs text-white truncate max-w-[70%]">{sourceName}</span>
        {relevanceScore && (
          <span className="text-[10px] uppercase font-bold tracking-wider text-brand-500 bg-brand-500/10 px-2 py-0.5 rounded-full border border-brand-500/20">
            {relevanceScore}% match
          </span>
        )}
      </div>
      <p className="text-xs text-ui-text-secondary leading-relaxed mt-3 line-clamp-3">
        "{excerpt}"
      </p>
    </Card>
  );
};

export default CitationCard;
