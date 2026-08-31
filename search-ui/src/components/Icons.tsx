import { FileText, MessageSquareQuote, Newspaper, NotebookPen } from 'lucide-react'
import type { DocType } from '../types'

/** Icônes issues de Lucide (ISC) : cf. https://lucide.dev */
const TYPE_ICONS = {
  depeche: Newspaper,
  article: FileText,
  note: NotebookPen,
  transcription: MessageSquareQuote,
} as const satisfies Record<DocType, unknown>

export function TypeIcon({ type, className }: { type: DocType; className?: string }) {
  const Icon = TYPE_ICONS[type]
  return <Icon className={className} strokeWidth={1.75} aria-hidden="true" />
}
