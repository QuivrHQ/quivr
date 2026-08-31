import { useEffect, useId, useMemo, useRef, useState } from 'react'
import { suggest } from '../lib/search'
import { Search, X } from 'lucide-react'

interface SearchBarProps {
  value: string
  onChange: (value: string) => void
  onSubmit: (value: string) => void
  placeholder: string
  autoFocus?: boolean
  inputRef?: React.RefObject<HTMLInputElement | null>
}

export function SearchBar({
  value,
  onChange,
  onSubmit,
  placeholder,
  autoFocus,
  inputRef,
}: SearchBarProps) {
  const listId = useId()
  const localRef = useRef<HTMLInputElement>(null)
  const ref = inputRef ?? localRef
  const containerRef = useRef<HTMLDivElement>(null)
  const [open, setOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(-1)

  const suggestions = useMemo(() => (value.trim().length >= 2 ? suggest(value) : []), [value])
  const visible = open && suggestions.length > 0

  useEffect(() => {
    setActiveIndex(-1)
  }, [value])

  useEffect(() => {
    if (!visible) return
    const onPointerDown = (event: PointerEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) setOpen(false)
    }
    document.addEventListener('pointerdown', onPointerDown)
    return () => document.removeEventListener('pointerdown', onPointerDown)
  }, [visible])

  const submit = (query: string) => {
    const trimmed = query.trim()
    if (!trimmed) return
    setOpen(false)
    setActiveIndex(-1)
    ref.current?.blur()
    onSubmit(trimmed)
  }

  const onKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      // Soumission explicite : ne dépend pas de la soumission implicite du formulaire.
      event.preventDefault()
      submit(visible && activeIndex >= 0 ? suggestions[activeIndex] : value)
      return
    }
    if (event.key === 'Escape') {
      if (visible) {
        event.stopPropagation()
        setOpen(false)
      }
      return
    }
    if (!visible) return
    if (event.key === 'ArrowDown') {
      event.preventDefault()
      setActiveIndex((index) => (index + 1) % suggestions.length)
    } else if (event.key === 'ArrowUp') {
      event.preventDefault()
      setActiveIndex((index) => (index <= 0 ? suggestions.length - 1 : index - 1))
    }
  }

  return (
    <div className="searchbar" ref={containerRef}>
      <form
        className="searchbar-field"
        role="search"
        onSubmit={(event) => {
          event.preventDefault()
          submit(activeIndex >= 0 ? suggestions[activeIndex] : value)
        }}
      >
        <Search className="searchbar-icon" strokeWidth={2} aria-hidden="true" />
        <input
          ref={ref}
          className="searchbar-input"
          type="search"
          value={value}
          placeholder={placeholder}
          autoFocus={autoFocus}
          autoComplete="off"
          spellCheck={false}
          enterKeyHint="search"
          aria-label="Rechercher dans le corpus"
          role="combobox"
          aria-expanded={visible}
          aria-controls={listId}
          aria-autocomplete="list"
          aria-activedescendant={activeIndex >= 0 ? `${listId}-${activeIndex}` : undefined}
          onChange={(event) => {
            onChange(event.target.value)
            setOpen(true)
          }}
          onFocus={() => setOpen(true)}
          onKeyDown={onKeyDown}
        />
        {value && (
          <button
            type="button"
            className="searchbar-clear"
            aria-label="Effacer la recherche"
            onClick={() => {
              onChange('')
              ref.current?.focus()
            }}
          >
            <X className="searchbar-clear-icon" strokeWidth={2} aria-hidden="true" />
          </button>
        )}
      </form>

      {visible && (
        <ul className="suggestions" id={listId} role="listbox" aria-label="Suggestions">
          {suggestions.map((suggestion, index) => (
            <li
              key={suggestion}
              id={`${listId}-${index}`}
              role="option"
              aria-selected={index === activeIndex}
              className={index === activeIndex ? 'suggestion is-active' : 'suggestion'}
              onMouseEnter={() => setActiveIndex(index)}
              onPointerDown={(event) => {
                event.preventDefault()
                onChange(suggestion)
                submit(suggestion)
              }}
            >
              <Search className="suggestion-icon" strokeWidth={2} aria-hidden="true" />
              <span>{suggestion}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
