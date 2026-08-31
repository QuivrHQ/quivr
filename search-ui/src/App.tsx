import { useEffect, useMemo, useRef, useState } from 'react'
import { AnswerCard } from './components/AnswerCard'
import { Brand } from './components/Logo'
import { DocumentPanel } from './components/DocumentPanel'
import { ModeSwitch } from './components/ModeSwitch'
import { Pagination } from './components/Pagination'
import { ResultItem } from './components/ResultItem'
import { SearchBar } from './components/SearchBar'
import { ResultsSkeleton } from './components/Skeleton'
import { composeAnswer } from './lib/agent'
import { formatNumber } from './lib/format'
import { fetchDocument, search, tokenize } from './lib/search'
import type { DocumentDetail, Mode, SearchResponse, SearchResult } from './types'

/** Résultats par page en mode recherche. */
const PER_PAGE = 10
/** Documents transmis à l’agent pour rédiger sa réponse. */
const AGENT_CONTEXT = 8

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
  mode: Mode
  doc: string | null
}

function readUrl(): UrlState {
  const params = new URLSearchParams(window.location.search)
  const page = Number.parseInt(params.get('page') ?? '1', 10)
  return {
    q: params.get('q') ?? '',
    page: Number.isFinite(page) && page > 0 ? page : 1,
    mode: params.get('mode') === 'agent' ? 'agent' : 'search',
    doc: params.get('doc'),
  }
}

function buildUrl({ q, page, mode, doc }: UrlState): string {
  const params = new URLSearchParams()
  if (q) params.set('q', q)
  if (mode !== 'search') params.set('mode', mode)
  if (page > 1 && !doc) params.set('page', String(page))
  if (doc) params.set('doc', doc)
  const query = params.toString()
  return query ? `?${query}` : window.location.pathname
}

export default function App() {
  const initial = useMemo(readUrl, [])
  const [input, setInput] = useState(initial.q)
  const [query, setQuery] = useState(initial.q)
  const [mode, setMode] = useState<Mode>(initial.mode)
  const [page, setPage] = useState(initial.page)
  const [results, setResults] = useState<SearchResult[]>([])
  const [response, setResponse] = useState<SearchResponse | null>(null)
  const [status, setStatus] = useState<Status>(initial.q ? 'loading' : 'idle')
  const [activeIndex, setActiveIndex] = useState(-1)
  const [docId, setDocId] = useState<string | null>(initial.doc)
  const [doc, setDoc] = useState<DocumentDetail | null>(null)
  const [docLoading, setDocLoading] = useState(Boolean(initial.doc))

  const inputRef = useRef<HTMLInputElement>(null)
  const itemRefs = useRef<Array<HTMLAnchorElement | null>>([])
  /** Élément à re-focaliser à la fermeture du panneau. */
  const openerRef = useRef<HTMLElement | null>(null)
  const terms = useMemo(() => tokenize(query), [query])
  const hasQuery = query.trim().length > 0

  const answer = useMemo(
    () => (mode === 'agent' && status === 'ready' ? composeAnswer(query, results) : null),
    [mode, status, query, results],
  )

  // La liste affichée : les sources citées en mode agent, la page de résultats sinon.
  const visibleResults = mode === 'agent' ? (answer?.sources ?? []) : results

  useEffect(() => {
    if (!hasQuery) {
      setResults([])
      setResponse(null)
      setStatus('idle')
      return
    }

    const controller = new AbortController()
    setStatus('loading')

    const request = {
      q: query,
      page: mode === 'agent' ? 1 : page,
      perPage: mode === 'agent' ? AGENT_CONTEXT : PER_PAGE,
    }

    search(request, controller.signal)
      .then((next) => {
        setResponse(next)
        setResults(next.results)
        setStatus('ready')
        if (mode === 'search' && next.page !== page) setPage(next.page)
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setStatus('error')
      })

    return () => controller.abort()
  }, [query, page, mode, hasQuery])

  useEffect(() => {
    if (!docId) {
      setDoc(null)
      setDocLoading(false)
      return
    }

    const controller = new AbortController()
    setDocLoading(true)

    fetchDocument(docId, controller.signal)
      .then((next) => {
        setDoc(next)
        setDocLoading(false)
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setDoc(null)
        setDocLoading(false)
      })

    return () => controller.abort()
  }, [docId])

  useEffect(() => {
    window.history.replaceState(null, '', buildUrl({ q: query, page, mode, doc: docId }))
    document.title = query ? `${query} — Quivr Search` : 'Quivr Search'
  }, [query, page, mode, docId])

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

      if (event.key === 'Escape') {
        if (docId) closeDocument()
        else if (isTyping) inputRef.current?.blur()
        return
      }

      if (docId || visibleResults.length === 0) return
      if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return
      if (isTyping && event.key === 'ArrowUp') return

      event.preventDefault()
      const step = event.key === 'ArrowDown' ? 1 : -1
      const next = Math.min(Math.max(activeIndex + step, 0), visibleResults.length - 1)
      setActiveIndex(next)
      const anchor = itemRefs.current[next]
      anchor?.focus({ preventScroll: true })
      anchor?.scrollIntoView({ block: 'nearest' })
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [activeIndex, visibleResults.length, docId])

  const runSearch = (value: string) => {
    setInput(value)
    setQuery(value)
    setPage(1)
    setActiveIndex(-1)
    setDocId(null)
    window.scrollTo({ top: 0 })
  }

  const changeMode = (next: Mode) => {
    setMode(next)
    setPage(1)
    setActiveIndex(-1)
    setDocId(null)
  }

  const changePage = (value: number) => {
    setPage(value)
    setActiveIndex(-1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const openDocument = (id: string) => {
    openerRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null
    setDocId(id)
  }

  const closeDocument = () => {
    setDocId(null)
    openerRef.current?.focus()
  }

  const goHome = () => {
    setInput('')
    setQuery('')
    setPage(1)
    setActiveIndex(-1)
    setDocId(null)
  }

  const searchBar = (
    <SearchBar
      value={input}
      onChange={setInput}
      onSubmit={runSearch}
      inputRef={inputRef}
      placeholder="Rechercher"
    />
  )

  if (!hasQuery) {
    return (
      <div className="app" data-view="home">
        <main className="home">
          <div className="home-inner">
            <h1 className="brand brand-hero">
              <Brand />
            </h1>

            <SearchBar
              value={input}
              onChange={setInput}
              onSubmit={runSearch}
              inputRef={inputRef}
              autoFocus
              placeholder="Rechercher"
            />

            <div className="home-mode">
              <ModeSwitch mode={mode} onChange={changeMode} />
            </div>

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

  const header = (
    <header className="topbar">
      <a
        className="brand brand-compact"
        href="/"
        onClick={(event) => {
          event.preventDefault()
          goHome()
        }}
      >
        <Brand />
      </a>
      <div className="topbar-main">
        {searchBar}
        <ModeSwitch mode={mode} onChange={changeMode} />
      </div>
    </header>
  )

  return (
    <div className="app" data-view="results">
      {header}

      <main className="results-page">
        <div className="results-head">
          <p className="results-count" role="status">
            {status === 'loading' && !response ? (
              <span className="results-count-placeholder">Recherche en cours…</span>
            ) : response ? (
              mode === 'agent' ? (
                <>
                  <strong>{formatNumber(answer?.sources.length ?? 0)}</strong> source
                  {(answer?.sources.length ?? 0) > 1 ? 's' : ''} citée
                  {(answer?.sources.length ?? 0) > 1 ? 's' : ''}
                  <span className="results-count-sep">·</span>
                  {formatNumber(response.total)} documents trouvés
                  <span className="results-count-sep">·</span>
                  {response.tookMs} ms
                </>
              ) : (
                <>
                  <strong>{formatNumber(response.total)}</strong>{' '}
                  {response.total > 1 ? 'résultats' : 'résultat'}
                  <span className="results-count-sep">·</span>
                  {response.tookMs} ms
                </>
              )
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

        {mode === 'agent' && status !== 'error' && (results.length > 0 || status === 'loading') && (
          <AnswerCard answer={answer} thinking={status === 'loading'} onOpenSource={openDocument} />
        )}

        {status === 'loading' && mode === 'search' && <ResultsSkeleton />}

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
                {mode === 'agent' && <h2 className="sources-title">Sources</h2>}

                <div className="results">
                  {visibleResults.map((result, index) => (
                    <ResultItem
                      key={result.id}
                      result={result}
                      terms={terms}
                      rank={mode === 'agent' ? index + 1 : undefined}
                      href={buildUrl({ q: query, page, mode, doc: result.id })}
                      onOpen={() => openDocument(result.id)}
                      active={index === activeIndex}
                      onActivate={() => setActiveIndex(index)}
                      ref={(node: HTMLElement | null) => {
                        itemRefs.current[index] = node as HTMLAnchorElement | null
                      }}
                    />
                  ))}
                </div>

                {mode === 'search' && (
                  <>
                    <Pagination page={response.page} totalPages={response.totalPages} onPageChange={changePage} />
                    <p className="page-status">
                      Page {formatNumber(response.page)} sur {formatNumber(response.totalPages)}
                    </p>
                  </>
                )}
              </>
            )}
          </>
        )}
      </main>

      {docId && (
        <DocumentPanel document={doc} terms={terms} loading={docLoading} onClose={closeDocument} />
      )}
    </div>
  )
}
