import "./LoadingSkeleton.css";

interface LoadingSkeletonProps {
  count?: number;
}

function LoadingSkeleton({ count = 3 }: LoadingSkeletonProps) {
  return (
    <ul className="skeleton-list">
      {Array.from({ length: count }, (_, i) => (
        <li key={i} className="skeleton-card" aria-hidden="true">
          <div className="skeleton-row skeleton-title" />
          <div className="skeleton-row-group">
            <div className="skeleton-row skeleton-tag" />
            <div className="skeleton-row skeleton-tag" />
            <div className="skeleton-row skeleton-tag" />
          </div>
        </li>
      ))}
    </ul>
  );
}

export default LoadingSkeleton;
