import React from 'react';
import Card from './Card';
import Badge from '../Feedback/Badge';
import Button from '../Buttons/Button';

const CitationCard = ({
  documentTitle = 'Untitled Document',
  source = 'Unknown Source',
  pageNumber,
  timestamp,
  confidence = 100, // percentage (e.g. 98)
  onOpen,
  className = '',
  ...props
}) => {
  return (
    <Card 
      className={`border border-ui-border bg-ui-surface/60 hover:bg-ui-surfaceHover hover:border-ui-borderHover transition-all flex flex-col justify-between h-full p-5 rounded-2xl ${className}`}
      {...props}
    >
      <div className="space-y-3">
        {/* Header: Title and Badge */}
        <div className="flex justify-between items-start gap-4">
          <h4 className="font-semibold text-sm text-ui-text-primary line-clamp-2 leading-snug">
            {documentTitle}
          </h4>
          <Badge variant={confidence >= 80 ? 'success' : confidence >= 50 ? 'warning' : 'danger'} size="sm">
            {confidence}% Match
          </Badge>
        </div>

        {/* Source metadata info */}
        <div className="text-xs text-ui-text-tertiary space-y-1">
          <div className="flex items-center gap-1">
            <span className="font-medium text-ui-text-secondary">Source:</span>
            <span className="truncate max-w-[180px]">{source}</span>
          </div>
          <div className="flex justify-between items-center text-[11px] pt-1">
            {pageNumber && (
              <span>Page {pageNumber}</span>
            )}
            {timestamp && (
              <span>{timestamp}</span>
            )}
          </div>
        </div>
      </div>

      {/* Open Button */}
      <div className="mt-4 pt-3 border-t border-ui-divider flex justify-end">
        <Button 
          variant="outline" 
          size="sm" 
          onClick={onOpen}
          className="text-xs font-semibold px-3 py-1.5 rounded-lg border-ui-border hover:bg-ui-surface"
        >
          Open Document
        </Button>
      </div>
    </Card>
  );
};

export default CitationCard;
