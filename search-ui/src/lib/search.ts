import { CORPUS, INDEX_SIZE, normalize, type CorpusDoc } from './corpus'
import type { SearchRequest, SearchResponse, SearchResult } from '../types'

export { INDEX_SIZE }

/** Date de référence du corpus factice (les documents sont antérieurs). */
const NOW = Date.parse('2026-08-31T00:00:00Z')

/** Mots outils : ignorés au scoring comme à la mise en évidence. */
const STOPWORDS = new Set([
  'au', 'aux', 'avec', 'ce', 'ces', 'cet', 'cette', 'comme', 'dans', 'de', 'des', 'du', 'elle',
  'elles', 'en', 'est', 'et', 'eux', 'il', 'ils', 'je', 'la', 'le', 'les', 'leur', 'leurs', 'lui',
  'ma', 'mais', 'me', 'mes', 'moins', 'mon', 'ne', 'nos', 'notre', 'nous', 'on', 'ont', 'ou', 'par',
  'pas', 'plus', 'pour', 'que', 'quel', 'quelle', 'qui', 'sa', 'sans', 'se', 'ses', 'son', 'sont',
  'sur', 'ta', 'te', 'tes', 'ton', 'tous', 'tout', 'toute', 'toutes', 'tu', 'un', 'une', 'vos',
  'votre', 'vous', 'and', 'for', 'the', 'with',
])

/** Découpe une requête en termes normalisés : sans accents, sans ponctuation, sans mots outils. */
export function tokenize(query: string): string[] {
  const tokens = normalize(query)
    .split(/[^a-z0-9]+/)
    .filter((term) => term.length > 1)
  const meaningful = tokens.filter((term) => !STOPWORDS.has(term))
  // Une requête composée uniquement de mots outils reste interrogeable telle quelle.
  return meaningful.length > 0 ? meaningful : tokens
}

function countOccurrences(haystack: string, term: string): number {
  let count = 0
  let index = haystack.indexOf(term)
  while (index !== -1) {
    count += 1
    index = haystack.indexOf(term, index + term.length)
  }
  return count
}

/**
 * Score brut. Le titre pèse davantage que le corps, l’expression exacte est
 * primée, et à pertinence égale un document récent passe devant : sur un fil
 * d’agence, la fraîcheur fait partie de la pertinence.
 */
function scoreDocument(doc: CorpusDoc, terms: string[], phrase: string): number {
  const title = normalize(doc.title)
  let raw = 0
  let matched = 0

  for (const term of terms) {
    const position = title.indexOf(term)
    const inTitle = countOccurrences(title, term)
    const inBody = countOccurrences(doc.haystack, term)
    if (inTitle === 0 && inBody === 0) continue
    matched += 1
    raw += inTitle * 6 + Math.min(inBody, 8) * 1.2
    // Un terme placé tôt dans le titre est plus significatif.
    if (position >= 0) raw += 2 * (1 - position / Math.max(title.length, 1))
  }

  if (matched === 0) return 0
  if (matched === terms.length) raw *= 1.6
  if (phrase.length > 2 && doc.haystack.includes(phrase)) raw += 8

  const ageDays = Math.max(0, (NOW - Date.parse(doc.publishedAt)) / 86400000)
  raw += 3 * Math.exp(-ageDays / 540)

  return raw
}

/** Pertinence affichée : position du document par rapport au meilleur résultat. */
function relativeScore(raw: number, best: number): number {
  if (best <= 0) return 0
  return Math.min(0.99, 0.99 * Math.pow(raw / best, 0.55))
}

/** Sélectionne les phrases du document qui portent le plus de termes de la requête. */
function buildSnippet(doc: CorpusDoc, terms: string[]): string {
  const sentences = doc.body.split(/(?<=\.)\s+/)
  const ranked = sentences
    .map((sentence, index) => {
      const normalized = normalize(sentence)
      const hits = terms.reduce((sum, term) => sum + (normalized.includes(term) ? 1 : 0), 0)
      return { sentence, index, hits }
    })
    .sort((a, b) => b.hits - a.hits || a.index - b.index)

  const picked = ranked.filter((entry) => entry.hits > 0).slice(0, 2)
  const chosen = (picked.length > 0 ? picked : ranked.slice(0, 1)).sort((a, b) => a.index - b.index)

  // Une seule phrase pertinente : on ajoute la phrase voisine en guise de contexte.
  if (chosen.length === 1) {
    const neighbourIndex = chosen[0].index + 1 < sentences.length ? chosen[0].index + 1 : chosen[0].index - 1
    if (neighbourIndex >= 0) {
      chosen.push({ sentence: sentences[neighbourIndex], index: neighbourIndex, hits: 0 })
      chosen.sort((a, b) => a.index - b.index)
    }
  }

  let snippet = chosen.map((entry) => entry.sentence).join(' ')
  if (snippet.length > 300) snippet = `${snippet.slice(0, 297).trimEnd()}…`
  return snippet
}

function toResult(doc: CorpusDoc, snippet: string, score: number): SearchResult {
  const { body: _body, haystack: _haystack, ...rest } = doc
  return { ...rest, snippet, score }
}

/**
 * Exécute une recherche sur le corpus local.
 *
 * C’est le seul point à remplacer pour brancher le backend : la signature
 * `(request) => Promise<SearchResponse>` est le contrat attendu par l’UI.
 */
export function search(request: SearchRequest, signal?: AbortSignal): Promise<SearchResponse> {
  const terms = tokenize(request.q)

  return new Promise((resolve, reject) => {
    // Latence simulée, pour que les états de chargement soient réalistes.
    const latency = 90 + Math.round(Math.random() * 220)
    const timer = setTimeout(() => {
      if (signal?.aborted) {
        reject(new DOMException('Recherche annulée', 'AbortError'))
        return
      }
      resolve(runQuery(request, terms, latency))
    }, latency)

    signal?.addEventListener('abort', () => {
      clearTimeout(timer)
      reject(new DOMException('Recherche annulée', 'AbortError'))
    })
  })
}

function runQuery(request: SearchRequest, terms: string[], latency: number): SearchResponse {
  const startedAt = performance.now()
  const { page, perPage } = request

  if (terms.length === 0) {
    return {
      results: [],
      total: 0,
      tookMs: latency,
      page,
      perPage,
      totalPages: 0,
    }
  }

  const phrase = normalize(request.q).trim()

  const scored: Array<{ doc: CorpusDoc; score: number }> = []
  let bestScore = 0
  for (const doc of CORPUS) {
    const score = scoreDocument(doc, terms, phrase)
    if (score > 0) {
      scored.push({ doc, score })
      if (score > bestScore) bestScore = score
    }
  }

  scored.sort((a, b) => b.score - a.score || Date.parse(b.doc.publishedAt) - Date.parse(a.doc.publishedAt))

  const total = scored.length
  const totalPages = Math.ceil(total / perPage)
  const safePage = Math.min(Math.max(page, 1), Math.max(totalPages, 1))
  const offset = (safePage - 1) * perPage

  return {
    results: scored
      .slice(offset, offset + perPage)
      .map((entry) => toResult(entry.doc, buildSnippet(entry.doc, terms), relativeScore(entry.score, bestScore))),
    total,
    tookMs: latency + Math.round(performance.now() - startedAt),
    page: safePage,
    perPage,
    totalPages,
  }
}

/** Slug d’agence en tête de titre (URGENT:, PAPIER GÉNÉRAL:…). */
const SLUG_PREFIX = /^[A-ZÉÈÀÇ]{2,}[A-ZÉÈÀÇ ]*: /

/** Complétions proposées sous la barre de recherche. */
export function suggest(query: string, limit = 6): string[] {
  const terms = tokenize(query)
  if (terms.length === 0) return []

  const seen = new Set<string>()
  const matches: Array<{ title: string; score: number }> = []

  for (const doc of CORPUS) {
    // On propose le titre nu : sans slug d’agence en tête, sans angle en fin.
    const base = doc.title.split(' — ')[0].replace(SLUG_PREFIX, '')
    if (seen.has(base)) continue
    const normalized = normalize(base)
    let score = 0
    for (const term of terms) {
      const index = normalized.indexOf(term)
      if (index === -1) {
        score = 0
        break
      }
      score += index === 0 ? 3 : 1
    }
    if (score > 0) {
      seen.add(base)
      matches.push({ title: base, score })
    }
  }

  return matches
    .sort((a, b) => b.score - a.score || a.title.length - b.title.length)
    .slice(0, limit)
    .map((entry) => entry.title)
}
