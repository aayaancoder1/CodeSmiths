import { useState, useEffect, useCallback } from 'react';

/**
 * Generic async data fetching hook.
 * Eliminates repetitive loading/error/data state in every page component.
 *
 * @param {Function} fn - Async function to call
 * @param {any[]} deps - Dependency array (re-runs when deps change)
 * @param {object} options
 * @param {any} options.initialData - Default value before first fetch
 * @returns {{ data, loading, error, refetch }}
 */
const useAsync = (fn, deps = [], { initialData = null } = {}) => {
  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const execute = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fn();
      setData(result);
    } catch (err) {
      console.error('[useAsync] Error:', err);
      setError(err?.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    execute();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [execute]);

  return { data, loading, error, refetch: execute };
};

export default useAsync;
