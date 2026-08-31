import type { SearchResult } from '../types'
import { normalize } from './corpus'

/**
 * Rédaction de la réponse du mode agent.
 *
 * Version bouchon : la réponse est composée à partir des passages les plus
 * pertinents des documents retrouvés, chaque affirmation portant le numéro de
 * sa source. Pour brancher un vrai modèle, remplacer `composeAnswer` par un
 * appel de génération auquel on passe la question et les extraits — le reste de
 * l’interface (marqueurs [n], liste des sources, ouverture du document) ne
 * change pas.
 */

export interface AgentAnswer {
  /** Texte de la réponse ; les citations y figurent sous la forme « [1] ». */
  text: string
  /** Sources citées, dans l’ordre des marqueurs. */
  sources: SearchResult[]
}

/** Étapes affichées pendant la préparation de la réponse. */
export const AGENT_STEPS = [
  'Interrogation de l’index',
  'Lecture des documents retrouvés',
  'Rédaction de la réponse',
]

const MAX_SOURCES = 5

/** Phrases de l’extrait, de la plus pertinente à la moins pertinente. */
function sentences(result: SearchResult): string[] {
  return result.snippet
    .split(/(?<=\.)\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean)
    .map((sentence) => (sentence.endsWith('.') ? sentence : `${sentence}.`))
}

export function composeAnswer(query: string, results: SearchResult[]): AgentAnswer | null {
  if (results.length === 0) return null

  const sources: SearchResult[] = []
  const claims: string[] = []
  const seen = new Set<string>()

  // Deux documents peuvent porter le même passage : on ne retient l’argument
  // qu’une fois, en se rabattant sur la phrase suivante du même document.
  for (const result of results) {
    if (sources.length >= MAX_SOURCES) break
    const sentence = sentences(result).find((candidate) => !seen.has(normalize(candidate)))
    if (!sentence) continue
    seen.add(normalize(sentence))
    sources.push(result)
    claims.push(`${sentence} [${sources.length}]`)
  }

  const intro = `Sur « ${query} », voici ce qui ressort des ${sources.length} document${
    sources.length > 1 ? 's' : ''
  } les plus pertinents du corpus.`

  const paragraphs = [intro]
  for (let index = 0; index < claims.length; index += 2) {
    paragraphs.push(claims.slice(index, index + 2).join(' '))
  }

  return { text: paragraphs.join('\n\n'), sources }
}
