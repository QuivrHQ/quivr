import { Article, Newspaper, Notebook, Quotes } from '@phosphor-icons/react'
import type { DocType } from '../types'

/** Icônes Phosphor (MIT) : cf. https://phosphoricons.com */
const TYPE_ICONS = {
  depeche: Newspaper,
  article: Article,
  note: Notebook,
  transcription: Quotes,
} as const satisfies Record<DocType, unknown>

export function TypeIcon({ type, className }: { type: DocType; className?: string }) {
  const Icon = TYPE_ICONS[type]
  return <Icon className={className} weight="bold" aria-hidden="true" />
}
