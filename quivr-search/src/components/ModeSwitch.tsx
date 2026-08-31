import type { Mode } from '../types'
import { ChatCenteredText, MagnifyingGlass } from '@phosphor-icons/react'

const MODES: Array<{ value: Mode; label: string }> = [
  { value: 'search', label: 'Recherche' },
  { value: 'agent', label: 'Agent' },
]

export function ModeSwitch({ mode, onChange }: { mode: Mode; onChange: (mode: Mode) => void }) {
  return (
    <div className="mode-switch" role="tablist" aria-label="Mode d’interrogation">
      {MODES.map((entry) => (
        <button
          key={entry.value}
          type="button"
          role="tab"
          aria-selected={mode === entry.value}
          className="mode"
          onClick={() => onChange(entry.value)}
        >
          {entry.value === 'search' ? (
            <MagnifyingGlass className="mode-icon" weight="bold" aria-hidden="true" />
          ) : (
            <ChatCenteredText className="mode-icon" weight="bold" aria-hidden="true" />
          )}
          <span className="mode-label">{entry.label}</span>
        </button>
      ))}
    </div>
  )
}
