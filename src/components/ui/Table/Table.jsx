import React from 'react';
import Spinner from '../Feedback/Spinner';
import EmptyState from '../Feedback/EmptyState';
import Pagination from './Pagination';

const Table = ({
  headers = [],
  data = [],
  renderRow,
  loading = false,
  emptyMessage = "No search results match current criteria.",
  onSort,
  sortBy,
  sortOrder = 'asc',
  currentPage = 1,
  totalPages = 1,
  onPageChange,
  className = '',
  ...props
}) => {
  const handleSort = (key) => {
    if (onSort) onSort(key);
  };

  return (
    <div className={`space-y-4 ${className}`} {...props}>
      <div className="overflow-x-auto rounded-xl border border-ui-border bg-ui-surface/30">
        <table className="min-w-full divide-y divide-ui-border text-left text-sm text-ui-text-secondary">
          <thead className="bg-ui-surface text-xs font-semibold text-ui-text-secondary uppercase tracking-wider">
            <tr>
              {headers.map((header) => {
                const isSortable = !!header.sortKey;
                const isSorted = sortBy === header.sortKey;

                return (
                  <th 
                    key={header.key || header.label} 
                    className={`px-6 py-4 font-semibold ${isSortable ? 'cursor-pointer hover:text-white select-none' : ''}`}
                    onClick={() => isSortable && handleSort(header.sortKey)}
                  >
                    <div className="flex items-center gap-1.5">
                      <span>{header.label}</span>
                      {isSortable && (
                        <span className="text-[10px] text-ui-text-tertiary">
                          {isSorted ? (sortOrder === 'asc' ? '▲' : '▼') : '↕'}
                        </span>
                      )}
                    </div>
                  </th>
                );
              })}
            </tr>
          </thead>
          
          <tbody className="divide-y divide-ui-divider bg-ui-bg/10">
            {loading ? (
              <tr>
                <td colSpan={headers.length} className="px-6 py-12">
                  <div className="flex justify-center items-center">
                    <Spinner size="md" />
                  </div>
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={headers.length} className="px-6 py-12 text-center">
                  <EmptyState 
                    title="No records found" 
                    description={emptyMessage}
                  />
                </td>
              </tr>
            ) : (
              data.map((item, index) => renderRow(item, index))
            )}
          </tbody>
        </table>
      </div>

      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={onPageChange}
      />
    </div>
  );
};

export default Table;
