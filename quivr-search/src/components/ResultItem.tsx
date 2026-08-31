import { forwardRef } from 'react'
import { TYPE_LABELS, type SearchResult } from '../types'
import { formatNumber, formatRelative } from '../lib/format'
import { Highlight } from './Highlight'
import { TypeIcon } from './Icons'

interface ResultItemProps {
  result: SearchResult
  terms: string[]
  active: boolean
  onActivate: () => void
  /** Numéro de citation, en mode agent uniquement. */
  rank?: number
  href: string
  onOpen: () => void
}

export const ResultItem = forwardRef<HTMLElement, ResultItemProps>(function ResultItem(
  { result, terms, active, onActivate, rank, href, onOpen },
  ref,
) {
  return (
    <article className="result" data-active={active || undefined} onMouseEnter={onActivate}>
      <div className="result-path">
        {rank ? <span className="result-rank">{rank}</span> : <TypeIcon type={result.type} className="result-path-icon" />}
        <span className="result-path-text">{result.path.join(' › ')}</span>
      </div>

      <h2 className="result-title">
        <a
          ref={ref as React.Ref<HTMLAnchorElement>}
          href={href}
          className="result-link"
          onClick={(event) => {
            // Un clic modifié (nouvel onglet) garde le comportement natif du lien.
            if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return
            event.preventDefault()
            onOpen()
          }}
        >
          <Highlight text={result.title} terms={terms} />
        </a>
      </h2>

      <p className="result-snippet">
        {/* Les documents internes n’ont pas de lieu de rédaction. */}
        {result.type !== 'note' && <span className="result-dateline">{result.bureau.toUpperCase()}</span>}
        <Highlight text={result.snippet} terms={terms} />
      </p>

      <div className="result-meta">
        <span>{TYPE_LABELS[result.type]}</span>
        <span>{result.author}</span>
        <span>{formatNumber(result.words)} mots</span>
        <span>{formatRelative(result.publishedAt)}</span>
        <span className="score" title="Pertinence relative au meilleur résultat">
          <span className="score-track" aria-hidden="true">
            <span className="score-fill" style={{ width: `${Math.round(result.score * 100)}%` }} />
          </span>
          {Math.round(result.score * 100)} %
        </span>
      </div>
    </article>
  )
})
