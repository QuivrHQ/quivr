const numberFormat = new Intl.NumberFormat('fr-FR')
const dateFormat = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })

export function formatNumber(value: number): string {
  return numberFormat.format(value)
}

export function formatCompact(value: number): string {
  if (value < 1000) return numberFormat.format(value)
  if (value < 1_000_000) return `${numberFormat.format(Math.round(value / 100) / 10)} k`
  return `${numberFormat.format(Math.round(value / 100_000) / 10)} M`
}

export function formatDate(iso: string): string {
  return dateFormat.format(new Date(iso))
}

/** « il y a 3 jours », « il y a 4 mois »… calculé par rapport à aujourd’hui. */
export function formatRelative(iso: string): string {
  const days = Math.floor((Date.now() - Date.parse(iso)) / 86400000)
  if (days <= 0) return 'aujourd’hui'
  if (days === 1) return 'hier'
  if (days < 30) return `il y a ${days} jours`
  const months = Math.floor(days / 30)
  if (months < 12) return `il y a ${months} mois`
  const years = Math.floor(days / 365)
  return years === 1 ? 'il y a 1 an' : `il y a ${years} ans`
}
