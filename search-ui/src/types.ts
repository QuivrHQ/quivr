/** Corpus 100 % texte pour l’instant : ni photo, ni vidéo. */
export type DocType = 'depeche' | 'article' | 'note' | 'transcription'

export type DocFeed =
  | 'Fil Monde'
  | 'Fil France'
  | 'Fil Éco'
  | 'Fil Sport'
  | 'AFP Factuel'
  | 'AFP Forum'
  | 'Archives'
  | 'Documentation rédaction'

export interface SearchResult {
  id: string
  title: string
  /** Fil d’Ariane : fil, rubrique, année. */
  path: string[]
  url: string
  /** Extrait du passage le plus pertinent. */
  snippet: string
  feed: DocFeed
  type: DocType
  /** Bureau AFP d’origine. */
  bureau: string
  /** Signature de la dépêche. */
  author: string
  /** ISO 8601. */
  publishedAt: string
  /** Longueur du document, en mots. */
  words: number
  /** Pertinence relative au meilleur résultat, entre 0 et 1. */
  score: number
}

export interface SearchRequest {
  q: string
  page: number
  perPage: number
}

export interface SearchResponse {
  results: SearchResult[]
  /** Nombre total de documents correspondants, toutes pages confondues. */
  total: number
  /** Temps de réponse du moteur, en millisecondes. */
  tookMs: number
  page: number
  perPage: number
  totalPages: number
}

export const TYPE_LABELS: Record<DocType, string> = {
  depeche: 'Dépêche',
  article: 'Article',
  note: 'Note',
  transcription: 'Transcription',
}
