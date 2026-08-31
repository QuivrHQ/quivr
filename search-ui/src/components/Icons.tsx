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

export function SparkIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 20 20" aria-hidden="true">
      <path
        d="M10 2.5 11.6 7 16 8.6 11.6 10.2 10 14.7 8.4 10.2 4 8.6 8.4 7z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinejoin="round"
      />
      <path d="M15.2 13.4 15.9 15.4 17.8 16.1 15.9 16.8 15.2 18.8 14.5 16.8 12.6 16.1 14.5 15.4z" fill="currentColor" />
    </svg>
  )
}

export function ArrowLeftIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 20 20" aria-hidden="true">
      <path d="M16 10H4.5M9 4.5 4 10l5 5.5" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
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
