import type { ReactNode } from 'react'
import type { DocType } from '../types'

interface IconProps {
  className?: string
}

export function SearchIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 20 20" aria-hidden="true">
      <circle cx="9" cy="9" r="6" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path d="M13.5 13.5 17.5 17.5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  )
}

export function ClearIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 20 20" aria-hidden="true">
      <path
        d="M5.5 5.5 14.5 14.5M14.5 5.5 5.5 14.5"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
    </svg>
  )
}

const TYPE_PATHS: Record<DocType, ReactNode> = {
  depeche: (
    <>
      <rect x="2.5" y="4.5" width="15" height="11" rx="1.5" fill="none" stroke="currentColor" strokeWidth="1.4" />
      <path d="M5.5 8h6M5.5 11h9M5.5 13.5h5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </>
  ),
  article: (
    <>
      <path d="M5 2.5h6l4 4v11H5z" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <path d="M11 2.5v4h4" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <path d="M7.5 10h5M7.5 13h5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </>
  ),
  note: (
    <>
      <path d="M4 3.5h9.5L16 6v10.5H4z" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <path d="M6.5 7.5h7M6.5 10.5h7M6.5 13.5h3.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </>
  ),
  transcription: (
    <>
      <path
        d="M16.5 12.5a1.5 1.5 0 0 1-1.5 1.5H8l-3.5 3V5a1.5 1.5 0 0 1 1.5-1.5h9a1.5 1.5 0 0 1 1.5 1.5z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinejoin="round"
      />
      <path d="M7.5 7.5h6M7.5 10.5h4" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </>
  ),
}

export function TypeIcon({ type, className }: { type: DocType; className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" aria-hidden="true">
      {TYPE_PATHS[type]}
    </svg>
  )
}
