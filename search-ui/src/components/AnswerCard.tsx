import { Fragment, useEffect, useMemo, useState } from 'react'
import { AGENT_STEPS, type AgentAnswer } from '../lib/agent'
import { SparkIcon } from './Icons'

interface AnswerCardProps {
  answer: AgentAnswer | null
  /** Vrai tant que la recherche tourne : on affiche les étapes de l’agent. */
  thinking: boolean
  onOpenSource: (id: string) => void
}

/** Vitesse de rédaction affichée, en mots par seconde. */
const WORDS_PER_SECOND = 34

function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

/** Rend un paragraphe en transformant les marqueurs « [n] » en citations cliquables. */
function withCitations(paragraph: string, answer: AgentAnswer, onOpenSource: (id: string) => void) {
  return paragraph.split(/(\[\d+\])/).map((chunk, index) => {
    const match = chunk.match(/^\[(\d+)\]$/)
    if (!match) return <Fragment key={index}>{chunk}</Fragment>

    const rank = Number.parseInt(match[1], 10)
    const source = answer.sources[rank - 1]
    if (!source) return <Fragment key={index}>{chunk}</Fragment>

    return (
      <button
        key={index}
        type="button"
        className="citation"
        title={source.title}
        aria-label={`Source ${rank} : ${source.title}`}
        onClick={() => onOpenSource(source.id)}
      >
        {rank}
      </button>
    )
  })
}

export function AnswerCard({ answer, thinking, onOpenSource }: AnswerCardProps) {
  const [step, setStep] = useState(0)
  const [revealed, setRevealed] = useState(0)

  // Les mots et les blancs sont conservés séparément : les marqueurs [n] restent entiers.
  const tokens = useMemo(() => (answer ? answer.text.split(/(\s+)/) : []), [answer])

  useEffect(() => {
    if (!thinking) return
    setStep(0)
    const timer = setInterval(() => setStep((current) => Math.min(current + 1, AGENT_STEPS.length - 1)), 320)
    return () => clearInterval(timer)
  }, [thinking])

  useEffect(() => {
    if (!answer) return
    if (prefersReducedMotion()) {
      setRevealed(tokens.length)
      return
    }
    setRevealed(0)
    // La progression est calculée sur le temps écoulé, pas sur le nombre de
    // tics : la réponse se termine même si l’onglet passe en arrière-plan.
    const startedAt = performance.now()
    const timer = setInterval(() => {
      const elapsed = (performance.now() - startedAt) / 1000
      const next = Math.min(tokens.length, Math.ceil(elapsed * WORDS_PER_SECOND) * 2)
      setRevealed(next)
      if (next >= tokens.length) clearInterval(timer)
    }, 30)
    return () => clearInterval(timer)
  }, [answer, tokens.length])

  if (thinking) {
    return (
      <section className="answer" aria-busy="true">
        <div className="answer-head">
          <SparkIcon className="answer-icon" />
          Réponse
        </div>
        <ol className="agent-steps">
          {AGENT_STEPS.map((label, index) => (
            <li key={label} className="agent-step" data-state={index < step ? 'done' : index === step ? 'active' : 'todo'}>
              {label}
            </li>
          ))}
        </ol>
      </section>
    )
  }

  if (!answer) return null

  const shown = tokens.slice(0, revealed).join('')
  const streaming = revealed < tokens.length

  return (
    <section className="answer">
      <div className="answer-head">
        <SparkIcon className="answer-icon" />
        Réponse
      </div>

      <div className="answer-body" data-streaming={streaming || undefined}>
        {shown.split('\n\n').map((paragraph, index) => (
          <p key={index}>{withCitations(paragraph, answer, onOpenSource)}</p>
        ))}
      </div>

      <p className="answer-note">
        Rédigée à partir des {answer.sources.length} sources ci-dessous. Chaque numéro ouvre le document
        d’origine.
      </p>
    </section>
  )
}
