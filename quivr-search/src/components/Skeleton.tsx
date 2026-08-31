export function ResultsSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="skeleton-list" aria-hidden="true">
      {Array.from({ length: count }, (_, index) => (
        <div className="skeleton-item" key={index}>
          <span className="skeleton-line" style={{ width: '32%' }} />
          <span className="skeleton-line skeleton-title" style={{ width: '58%' }} />
          <span className="skeleton-line" style={{ width: '96%' }} />
          <span className="skeleton-line" style={{ width: '74%' }} />
        </div>
      ))}
    </div>
  )
}
