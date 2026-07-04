import React from 'react';

const Pagination = ({
  currentPage = 1,
  totalPages = 1,
  onPageChange,
  className = '',
  ...props
}) => {
  if (totalPages <= 1) return null;

  const handlePrev = () => {
    if (currentPage > 1 && onPageChange) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages && onPageChange) {
      onPageChange(currentPage + 1);
    }
  };

  return (
    <div
      className={`flex items-center justify-between px-4 py-3 border border-ui-border rounded-xl bg-ui-surface/20 ${className}`}
      {...props}
    >
      <div className="text-xs text-ui-text-tertiary">
        Page <span className="font-semibold text-ui-text-secondary">{currentPage}</span> of{' '}
        <span className="font-semibold text-ui-text-secondary">{totalPages}</span>
      </div>
      <div className="flex gap-2">
        <button
          onClick={handlePrev}
          disabled={currentPage === 1}
          className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-ui-surface border border-ui-border text-ui-text-secondary hover:text-ui-text-primary hover:border-ui-borderHover disabled:opacity-40 disabled:pointer-events-none transition-colors"
        >
          Previous
        </button>
        <button
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-ui-surface border border-ui-border text-ui-text-secondary hover:text-ui-text-primary hover:border-ui-borderHover disabled:opacity-40 disabled:pointer-events-none transition-colors"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default Pagination;
