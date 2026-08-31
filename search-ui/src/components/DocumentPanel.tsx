import { useEffect, useRef } from 'react'
import { X } from 'lucide-react'
import { TYPE_LABELS, type DocumentDetail } from '../types'
import { formatDate, formatNumber } from '../lib/format'
import { Highlight } from './Highlight'
import { TypeIcon } from './Icons'

interface DocumentPanelProps {
  document: DocumentDetail | null
  terms: string[]
  loading: boolean
  onClose: () => void
}

/** Panneau latéral : le document s’ouvre sur la droite, les résultats restent visibles derrière. */
export function DocumentPanel({ document: detail, terms, loading, onClose }: DocumentPanelProps) {
  const panelRef = useRef<HTMLElement>(null)

  useEffect(() => {
    panelRef.current?.focus()
    // Le fond ne défile pas tant que le panneau est ouvert.
    const previous = window.document.body.style.overflow
    window.document.body.style.overflow = 'hidden'
    return () => {
      window.document.body.style.overflow = previous
    }
  }, [])

  return (
    <>
      <div className="drawer-backdrop" onClick={onClose} aria-hidden="true" />

      <aside
        className="drawer"
        role="dialog"
        aria-modal="true"
        aria-label="Document source"
        tabIndex={-1}
        ref={panelRef}
      >
        <header className="drawer-head">
          <span className="drawer-label">Source</span>
          <button type="button" className="drawer-close" onClick={onClose} aria-label="Fermer le document">
            <X className="drawer-close-icon" strokeWidth={2} aria-hidden="true" />
          </button>
        </header>

        <div className="drawer-body">
          {loading && (
            <div className="skeleton-list" aria-hidden="true">
              <div className="skeleton-item">
                <span className="skeleton-line" style={{ width: '38%' }} />
                <span className="skeleton-line skeleton-title" style={{ width: '86%' }} />
                <span className="skeleton-line" style={{ width: '100%' }} />
                <span className="skeleton-line" style={{ width: '94%' }} />
                <span className="skeleton-line" style={{ width: '97%' }} />
              </div>
            </div>
          )}

          {!loading && !detail && (
            <div className="empty">
              <h2>Document introuvable</h2>
              <p>Ce document n’est plus présent dans l’index.</p>
            </div>
          )}

          {!loading && detail && (
            <article className="document">
              <div className="result-path">
                <TypeIcon type={detail.type} className="result-path-icon" />
                <span className="result-path-text">{detail.path.join(' › ')}</span>
              </div>

              <h1 className="document-title">
                <Highlight text={detail.title} terms={terms} />
              </h1>

              <div className="result-meta document-meta">
                <span>{TYPE_LABELS[detail.type]}</span>
                <span>{detail.author}</span>
                <span>{detail.bureau}</span>
                <span>{formatNumber(detail.words)} mots</span>
                <span>{formatDate(detail.publishedAt)}</span>
              </div>

              <div className="document-body">
                {detail.paragraphs.map((paragraph, index) => (
                  <p key={index}>
                    {index === 0 && detail.type !== 'note' && (
                      <span className="result-dateline">
                        {detail.bureau.toUpperCase()}, {formatDate(detail.publishedAt)} (AFP) —
                      </span>
                    )}
                    <Highlight text={paragraph} terms={terms} />
                  </p>
                ))}
              </div>
            </article>
          )}
        </div>
      </aside>
    </>
  )
}
