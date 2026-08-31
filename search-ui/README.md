# Quivr Search UI

Front de recherche pour un RAG documentaire à grande échelle : une barre de
recherche, une liste de résultats, une pagination. Aucun filtre, rien d’autre.

Le backend n’est pas branché : les données viennent d’un corpus factice de
type agence de presse (dépêches, articles, notes de rédaction, transcriptions),
généré en local et **exclusivement textuel**.

## Démarrer

```bash
npm install
npm run dev
```

Le serveur écoute sur <http://localhost:5182> (port réservé pour ce projet).

| Commande            | Effet                                  |
| ------------------- | -------------------------------------- |
| `npm run dev`       | Serveur de développement Vite          |
| `npm run build`     | Vérification des types + build de prod |
| `npm run preview`   | Sert le build de production            |
| `npm run typecheck` | Types uniquement                       |

## Pile technique

Vite + React 19 + TypeScript, et **une seule feuille de style CSS**. Aucune
librairie d’UI, aucun framework CSS, aucune dépendance runtime en dehors de
React. Thème clair et sombre automatiques (`prefers-color-scheme`).

## Structure

```
src/
  App.tsx                  état de la recherche, URL, raccourcis clavier
  styles.css               tous les styles (jetons de couleur en tête de fichier)
  types.ts                 contrat de données (SearchRequest / SearchResponse)
  lib/
    search.ts              moteur de recherche factice  ← point de branchement
    corpus.ts              corpus de démonstration, généré de façon déterministe
    format.ts              formats nombres et dates (fr-FR)
  components/
    SearchBar.tsx          champ + suggestions (navigation clavier)
    ResultItem.tsx         un résultat
    Pagination.tsx         pagination 10 par 10
    Highlight.tsx          mise en évidence des termes, insensible aux accents
    Skeleton.tsx           état de chargement
    Icons.tsx              icônes SVG en ligne
```

## Brancher le vrai backend

Un seul point à remplacer : la fonction `search` de `src/lib/search.ts`. Elle
respecte déjà le contrat attendu par l’interface.

```ts
export async function search(request: SearchRequest, signal?: AbortSignal): Promise<SearchResponse> {
  const response = await fetch('/api/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal,
  })
  if (!response.ok) throw new Error('Recherche indisponible')
  return response.json()
}
```

```ts
interface SearchRequest {
  q: string
  page: number       // 1-indexé
  perPage: number    // 10
}

interface SearchResponse {
  results: SearchResult[]
  total: number      // nombre total de documents correspondants
  tookMs: number     // affiché à côté du nombre de résultats
  page: number
  perPage: number
  totalPages: number
}
```

`suggest()` (complétions sous le champ) est à remplacer de la même manière, ou
à supprimer si l’API n’en propose pas.

Une fois branché, `src/lib/corpus.ts` peut être supprimé : c’est le seul fichier
qui contient des données fictives.

## Détails d’implémentation

- **URL partageable** : `?q=…&page=…`. L’état est écrit en
  `replaceState`, donc le bouton « précédent » du navigateur ne rejoue pas
  l’historique de recherche.
- **Requête annulable** : chaque recherche reçoit un `AbortSignal`, les réponses
  périmées sont ignorées.
- **Pertinence** : le score affiché est relatif au meilleur résultat de la
  requête, pas une probabilité absolue.
- **Raccourcis** : `/` ou `⌘K` pour le champ, `↑` `↓` pour parcourir les
  résultats, `Échap` pour sortir du champ.
- **Accessibilité** : combobox ARIA sur les suggestions, `role="status"` sur le
  compteur de résultats, focus visible, `prefers-reduced-motion` respecté.
