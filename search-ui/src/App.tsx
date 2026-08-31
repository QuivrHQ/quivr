import { useEffect, useMemo, useRef, useState } from 'react'
import { Pagination } from './components/Pagination'
import { ResultItem } from './components/ResultItem'
import { SearchBar } from './components/SearchBar'
import { ResultsSkeleton } from './components/Skeleton'
import { formatCompact, formatNumber } from './lib/format'
import { INDEX_SIZE, search, tokenize } from './lib/search'
import type { SearchResponse, SearchResult } from './types'

const PER_PAGE = 10

const EXAMPLES = [
  'inflation',
  'cessez-le-feu',
  'intelligence artificielle',
  'jeux olympiques',
  'charte déontologique',
]

type Status = 'idle' | 'loading' | 'ready' | 'error'

interface UrlState {
  q: string
  page: number
}

function readUrl(): UrlState {
  const params = new URLSearchParams(window.location.search)
  const page = Number.parseInt(params.get('page') ?? '1', 10)
  return {
    q: params.get('q') ?? '',
    page: Number.isFinite(page) && page > 0 ? page : 1,
  }
}

function writeUrl({ q, page }: UrlState) {
  const params = new URLSearchParams()
  if (q) params.set('q', q)
  if (page > 1) params.set('page', String(page))
  const query = params.toString()
  window.history.replaceState(null, '', query ? `?${query}` : window.location.pathname)
}

export default function App() {
  const initial = useMemo(readUrl, [])
  const [input, setInput] = useState(initial.q)
  const [query, setQuery] = useState(initial.q)
  const [page, setPage] = useState(initial.page)
  const [results, setResults] = useState<SearchResult[]>([])
  const [response, setResponse] = useState<SearchResponse | null>(null)
  const [status, setStatus] = useState<Status>(initial.q ? 'loading' : 'idle')
  const [activeIndex, setActiveIndex] = useState(-1)

  const inputRef = useRef<HTMLInputElement>(null)
  const itemRefs = useRef<Array<HTMLAnchorElement | null>>([])
  const terms = useMemo(() => tokenize(query), [query])
  const hasQuery = query.trim().length > 0

  useEffect(() => {
    if (!hasQuery) {
      setResults([])
      setResponse(null)
      setStatus('idle')
      return
    }

    const controller = new AbortController()
    setStatus('loading')

    search({ q: query, page, perPage: PER_PAGE }, controller.signal)
      .then((next) => {
        setResponse(next)
        setResults(next.results)
        setStatus('ready')
        if (next.page !== page) setPage(next.page)
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setStatus('error')
      })

    return () => controller.abort()
  }, [query, page, hasQuery])

  useEffect(() => {
    writeUrl({ q: query, page })
    document.title = query ? `${query} — Quivr Search` : 'Quivr Search'
  }, [query, page])

  // Raccourcis clavier : « / » ou ⌘K pour la recherche, flèches pour parcourir.
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const target = event.target
      const isTyping =
        target instanceof HTMLElement &&
        (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable)

      if ((event.key === '/' && !isTyping) || ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k')) {
        event.preventDefault()
        inputRef.current?.focus()
        inputRef.current?.select()
        return
      }

      if (event.key === 'Escape' && isTyping) {
        inputRef.current?.blur()
        return
      }

      if (results.length === 0) return
      if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return
      if (isTyping && event.key === 'ArrowUp') return

      event.preventDefault()
      const step = event.key === 'ArrowDown' ? 1 : -1
      const next = Math.min(Math.max(activeIndex + step, 0), results.length - 1)
      setActiveIndex(next)
      const anchor = itemRefs.current[next]
      anchor?.focus({ preventScroll: true })
      anchor?.scrollIntoView({ block: 'nearest' })
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [activeIndex, results.length])

  const runSearch = (value: string) => {
    setInput(value)
    setQuery(value)
    setPage(1)
    setActiveIndex(-1)
    window.scrollTo({ top: 0 })
  }

  const changePage = (value: number) => {
    setPage(value)
    setActiveIndex(-1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const goHome = () => {
    setInput('')
    setQuery('')
    setPage(1)
    setActiveIndex(-1)
  }

  if (!hasQuery) {
    return (
      <div className="app" data-view="home">
        <main className="home">
          <div className="home-inner">
            <h1 className="brand brand-hero">
              Quivr <span>Search</span>
            </h1>
            <p className="home-tagline">
              Recherche sémantique sur {formatCompact(INDEX_SIZE)} de dépêches, articles et documents de rédaction.
            </p>

            <SearchBar
              value={input}
              onChange={setInput}
              onSubmit={runSearch}
              inputRef={inputRef}
              autoFocus
              placeholder="Rechercher une dépêche, un sujet, un document…"
            />

            <div className="examples">
              <span className="examples-label">Essayez</span>
              {EXAMPLES.map((example) => (
                <button key={example} type="button" className="chip" onClick={() => runSearch(example)}>
                  {example}
                </button>
              ))}
            </div>
          </div>

          <footer className="home-footer">
            <span>
              <kbd>/</kbd> pour rechercher · <kbd>↑</kbd> <kbd>↓</kbd> pour parcourir les résultats
            </span>
          </footer>
        </main>
      </div>
    )
  }

  return (
    <div className="app" data-view="results">
      <header className="topbar">
        <a
          className="brand brand-compact"
          href="/"
          onClick={(event) => {
            event.preventDefault()
            goHome()
          }}
        >
          Quivr <span>Search</span>
        </a>
        <SearchBar
          value={input}
          onChange={setInput}
          onSubmit={runSearch}
          inputRef={inputRef}
          placeholder="Rechercher une dépêche, un sujet, un document…"
        />
      </header>

      <main className="results-page">
        <div className="results-head">
          <p className="results-count" role="status">
            {status === 'loading' && !response ? (
              <span className="results-count-placeholder">Recherche en cours…</span>
            ) : response ? (
              <>
                <strong>{formatNumber(response.total)}</strong>{' '}
                {response.total > 1 ? 'résultats' : 'résultat'}
                <span className="results-count-sep">·</span>
                {response.tookMs} ms
              </>
            ) : null}
          </p>
        </div>

        {status === 'error' && (
          <div className="notice" role="alert">
            <p>La recherche a échoué.</p>
            <button type="button" className="button" onClick={() => runSearch(query)}>
              Réessayer
            </button>
          </div>
        )}

        {status === 'loading' && <ResultsSkeleton />}

        {status === 'ready' && response && (
          <>
            {results.length === 0 ? (
              <div className="empty">
                <h2>Aucun document ne correspond à « {query} »</h2>
                <ul>
                  <li>Vérifiez l’orthographe des termes employés.</li>
                  <li>Essayez des mots-clés plus généraux.</li>
                  <li>Utilisez moins de termes à la fois.</li>
                </ul>
              </div>
            ) : (
              <>
                <div className="results">
                  {results.map((result, index) => (
                    <ResultItem
                      key={result.id}
                      result={result}
                      terms={terms}
                      active={index === activeIndex}
                      onActivate={() => setActiveIndex(index)}
                      ref={(node: HTMLElement | null) => {
                        itemRefs.current[index] = node as HTMLAnchorElement | null
                      }}
                    />
                  ))}
                </div>

                <Pagination page={response.page} totalPages={response.totalPages} onPageChange={changePage} />

                <p className="page-status">
                  Page {formatNumber(response.page)} sur {formatNumber(response.totalPages)}
                </p>
              </>
            )}
          </>
        )}
      </main>
    </div>
  )
}
