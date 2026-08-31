import type { Mode } from '../types'
import { SearchIcon, SparkIcon } from './Icons'

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
            <SearchIcon className="mode-icon" />
          ) : (
            <SparkIcon className="mode-icon" />
          )}
          {entry.label}
        </button>
      ))}
    </div>
  )
}
