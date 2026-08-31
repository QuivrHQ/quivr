import { TYPE_LABELS, type DocumentDetail } from '../types'
import { formatDate, formatNumber } from '../lib/format'
import { ArrowLeftIcon, TypeIcon } from './Icons'
import { Highlight } from './Highlight'

interface DocumentViewProps {
  document: DocumentDetail | null
  terms: string[]
  loading: boolean
  onBack: () => void
}

export function DocumentView({ document, terms, loading, onBack }: DocumentViewProps) {
  return (
    <main className="document-page">
      <button type="button" className="back" onClick={onBack}>
        <ArrowLeftIcon className="back-icon" />
        Retour aux résultats
      </button>

      {loading && (
        <div className="skeleton-list" aria-hidden="true">
          <div className="skeleton-item">
            <span className="skeleton-line" style={{ width: '30%' }} />
            <span className="skeleton-line skeleton-title" style={{ width: '70%' }} />
            <span className="skeleton-line" style={{ width: '100%' }} />
            <span className="skeleton-line" style={{ width: '92%' }} />
            <span className="skeleton-line" style={{ width: '96%' }} />
          </div>
        </div>
      )}

      {!loading && !document && (
        <div className="empty">
          <h2>Document introuvable</h2>
          <p>Ce document n’est plus présent dans l’index.</p>
        </div>
      )}

      {!loading && document && (
        <article className="document">
          <div className="result-path">
            <TypeIcon type={document.type} className="result-path-icon" />
            <span className="result-path-text">{document.path.join(' › ')}</span>
          </div>

          <h1 className="document-title">
            <Highlight text={document.title} terms={terms} />
          </h1>

          <div className="result-meta document-meta">
            <span>{TYPE_LABELS[document.type]}</span>
            <span>{document.author}</span>
            <span>{document.bureau}</span>
            <span>{formatNumber(document.words)} mots</span>
            <span>{formatDate(document.publishedAt)}</span>
          </div>

          <div className="document-body">
            {document.paragraphs.map((paragraph, index) => (
              <p key={index}>
                {index === 0 && document.type !== 'note' && (
                  <span className="result-dateline">
                    {document.bureau.toUpperCase()}, {formatDate(document.publishedAt)} (AFP) —
                  </span>
                )}
                <Highlight text={paragraph} terms={terms} />
              </p>
            ))}
          </div>
        </article>
      )}
    </main>
  )
}
