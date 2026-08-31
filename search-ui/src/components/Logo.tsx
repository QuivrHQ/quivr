import { Feather } from 'lucide-react'

/**
 * Lockup de marque : pastille accentuée + nom du produit.
 * « Quivr » porte la marque, « Search » qualifie l’outil.
 */
export function Brand() {
  return (
    <>
      <span className="brand-badge">
        <Feather className="brand-badge-icon" strokeWidth={2} aria-hidden="true" />
      </span>
      <span className="brand-text">
        Quivr <span>Search</span>
      </span>
    </>
  )
}
