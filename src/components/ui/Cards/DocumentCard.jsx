import React from 'react';
import Card from './Card';

const DocumentCard = ({
  fileName,
  fileSize,
  fileType = 'PDF',
  status = 'ready', // 'ready' | 'processing' | 'failed'
  onClick,
  className = '',
  ...props
}) => {
  const statusColor = {
    ready: 'text-ui-success-solid bg-ui-success-bg/10 border-ui-success-border/20',
    processing: 'text-brand-500 bg-brand-500/10 border-brand-500/20 animate-pulse',
    failed: 'text-ui-danger-solid bg-ui-danger-bg/10 border-ui-danger-border/20',
  };

  return (
    <Card 
      onClick={onClick}
      className={`hover:border-ui-borderHover ${className}`}
      {...props}
    >
      <div className="flex items-center gap-3">
        {/* Document Icon Box */}
        <div className="w-10 h-10 rounded-lg bg-ui-bg border border-ui-border flex items-center justify-center font-bold text-xs text-brand-500 select-none">
          {fileType.toUpperCase()}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <h5 className="text-sm font-semibold text-white truncate">{fileName}</h5>
          {fileSize && <p className="text-xs text-ui-text-tertiary mt-0.5">{fileSize}</p>}
        </div>

        {/* Status Badge */}
        <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider border ${statusColor[status]}`}>
          {status}
        </span>
      </div>
    </Card>
  );
};

export default DocumentCard;
