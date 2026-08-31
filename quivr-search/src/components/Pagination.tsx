interface PaginationProps {
  page: number
  totalPages: number
  onPageChange: (page: number) => void
}

/** Fenêtre de pages affichée autour de la page courante. */
function pageWindow(page: number, totalPages: number, size = 7): number[] {
  const half = Math.floor(size / 2)
  let start = Math.max(1, page - half)
  const end = Math.min(totalPages, start + size - 1)
  start = Math.max(1, end - size + 1)
  return Array.from({ length: end - start + 1 }, (_, index) => start + index)
}

export function Pagination({ page, totalPages, onPageChange }: PaginationProps) {
  if (totalPages <= 1) return null
  const pages = pageWindow(page, totalPages)

  return (
    <nav className="pagination" aria-label="Pagination des résultats">
      <button
        type="button"
        className="page-arrow"
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
        aria-label="Page précédente"
      >
        ‹ Précédent
      </button>

      <ul className="page-list">
        {pages[0] > 1 && (
          <>
            <li>
              <button type="button" className="page" onClick={() => onPageChange(1)}>
                1
              </button>
            </li>
            {pages[0] > 2 && <li className="page-gap">…</li>}
          </>
        )}

        {pages.map((value) => (
          <li key={value}>
            <button
              type="button"
              className="page"
              aria-current={value === page ? 'page' : undefined}
              onClick={() => onPageChange(value)}
            >
              {value}
            </button>
          </li>
        ))}

        {pages[pages.length - 1] < totalPages && (
          <>
            {pages[pages.length - 1] < totalPages - 1 && <li className="page-gap">…</li>}
            <li>
              <button type="button" className="page" onClick={() => onPageChange(totalPages)}>
                {totalPages}
              </button>
            </li>
          </>
        )}
      </ul>

      <button
        type="button"
        className="page-arrow"
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
        aria-label="Page suivante"
      >
        Suivant ›
      </button>
    </nav>
  )
}
