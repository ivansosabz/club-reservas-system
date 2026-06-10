import { useCallback, useEffect, useRef, useState } from "react";

interface UseAsyncResult<T> {
  data: T | null;
  loading: boolean;
  error: string;
  setData: (data: T) => void;
  refresh: () => void;
}

export function useAsync<T>(
  fn: () => Promise<T>,
  deps: unknown[] = []
): UseAsyncResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  const execute = useCallback(() => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setLoading(true);
    setError("");

    const signal = controller.signal;

    fn()
      .then((result) => {
        if (!signal.aborted) {
          setData(result);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!signal.aborted) {
          setError(
            err instanceof Error ? err.message : "Ocurrio un error inesperado."
          );
          setLoading(false);
        }
      });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    execute();

    return () => {
      abortRef.current?.abort();
    };
  }, [execute]);

  return { data, loading, error, setData, refresh: execute };
}
