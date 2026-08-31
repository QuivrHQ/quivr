# Quivr Search UI

Front de recherche pour un RAG documentaire à grande échelle. Deux modes :

- **Recherche** — la liste des documents classés par pertinence, paginée 10 par 10 ;
- **Agent** — une réponse rédigée à partir des documents retrouvés, chaque
  affirmation portant le numéro de sa source.

Un clic sur un résultat ou sur un numéro de citation ouvre le **document
complet** dans un panneau latéral, par-dessus les résultats floutés, termes de
la requête surlignés.

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
librairie d’UI, aucun framework CSS ; deux dépendances runtime seulement :
React et [Phosphor](https://phosphoricons.com) pour les icônes. Thème clair et sombre
automatiques (`prefers-color-scheme`).

## Structure

```
src/
  App.tsx                  état (mode, requête, page, document), URL, raccourcis
  styles.css               tous les styles (jetons de couleur en tête de fichier)
  types.ts                 contrat de données (SearchRequest / SearchResponse…)
  lib/
    search.ts              moteur de recherche factice   ← point de branchement
    agent.ts               rédaction de la réponse citée ← point de branchement
    corpus.ts              corpus de démonstration, généré de façon déterministe
    format.ts              formats nombres et dates (fr-FR)
  components/
    SearchBar.tsx          champ + suggestions (navigation clavier)
    ModeSwitch.tsx         bascule Recherche / Agent
    AnswerCard.tsx         réponse de l’agent, citations cliquables
    DocumentPanel.tsx      document complet, en panneau latéral
    Logo.tsx               lockup de marque
    ResultItem.tsx         un résultat (numéroté en mode agent)
    Pagination.tsx         pagination 10 par 10
    Highlight.tsx          mise en évidence des termes, insensible aux accents
    Skeleton.tsx           état de chargement
    Icons.tsx              icônes de type de document (Phosphor)
```

## Brancher le vrai backend

Trois fonctions à remplacer, toutes isolées dans `src/lib/`. Elles respectent
déjà les contrats attendus par l’interface.

### 1. La recherche — `search()` dans `src/lib/search.ts`

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
  perPage: number    // 10 en mode recherche, 8 en mode agent
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

### 2. Le document complet — `fetchDocument()` dans `src/lib/search.ts`

```ts
export async function fetchDocument(id: string, signal?: AbortSignal): Promise<DocumentDetail | null> {
  const response = await fetch(`/api/documents/${id}`, { signal })
  if (response.status === 404) return null
  if (!response.ok) throw new Error('Document indisponible')
  return response.json()
}
```

`DocumentDetail` reprend les métadonnées d’un résultat et remplace l’extrait par
`paragraphs: string[]`.

### 3. La réponse de l’agent — `composeAnswer()` dans `src/lib/agent.ts`

Version actuelle : la réponse est assemblée à partir des passages retrouvés.
Version cible : un appel de génération auquel on transmet la question et les
extraits, en demandant au modèle de citer ses sources sous la forme `[n]`.
L’interface (marqueurs, liste des sources, ouverture du document) ne change pas.

```ts
export interface AgentAnswer {
  text: string             // « … entre en application en 2027. [1] »
  sources: SearchResult[]  // sources dans l’ordre des marqueurs
}
```

`suggest()` (complétions sous le champ) est à remplacer de la même manière, ou
à supprimer si l’API n’en propose pas.

Une fois branché, `src/lib/corpus.ts` peut être supprimé : c’est le seul fichier
qui contient des données fictives.

## Détails d’implémentation

- **URL partageable** : `?q=…&mode=agent&page=…&doc=…`. L’état est écrit en
  `replaceState`, donc le bouton « précédent » du navigateur ne rejoue pas
  l’historique de recherche. Un ⌘-clic sur un résultat ouvre bien le document
  dans un nouvel onglet.
- **Réponse progressive** : le texte de l’agent se dévoile à vitesse constante
  (34 mots/s), calculée sur le temps écoulé — elle se termine même si l’onglet
  passe en arrière-plan, et s’affiche d’un bloc si le système demande à réduire
  les animations.
- **Requête annulable** : chaque recherche reçoit un `AbortSignal`, les réponses
  périmées sont ignorées.
- **Pertinence** : le score affiché est relatif au meilleur résultat de la
  requête, pas une probabilité absolue.
- **Raccourcis** : `/` ou `⌘K` pour le champ, `↑` `↓` pour parcourir les
  résultats, `Échap` pour refermer le panneau ou sortir du champ.
- **Panneau latéral** : dialogue modal (`role="dialog"`), fond figé pendant
  l’ouverture, fermeture au clic sur le fond, et retour du focus sur le
  résultat d’origine.
- **Accessibilité** : combobox ARIA sur les suggestions, `role="status"` sur le
  compteur de résultats, focus visible, `prefers-reduced-motion` respecté.
