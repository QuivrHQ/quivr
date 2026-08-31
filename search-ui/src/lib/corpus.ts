import type { DocFeed, DocType, DocumentMeta } from '../types'

/**
 * Corpus factice de type agence de presse (dépêches, articles, notes de
 * rédaction, transcriptions). Uniquement du texte.
 *
 * Il est généré de façon déterministe : deux chargements produisent
 * exactement les mêmes documents, ce qui rend l’UI reproductible.
 */

/** Générateur pseudo-aléatoire déterministe (mulberry32). */
function makeRandom(seed: number) {
  let a = seed
  return () => {
    a |= 0
    a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

interface Desk {
  feed: DocFeed
  rubrique: string
  types: DocType[]
  titles: string[]
  sentences: string[]
}

const DESKS: Desk[] = [
  {
    feed: 'Fil France',
    rubrique: 'Politique',
    types: ['depeche', 'depeche', 'article', 'transcription'],
    titles: [
      'Budget: le gouvernement engage sa responsabilité devant l’Assemblée',
      'Réforme des retraites: les syndicats appellent à une nouvelle journée d’action',
      'Remaniement: quatre ministères changent de titulaire',
      'Élections municipales: les principaux enseignements du premier tour',
      'Motion de censure: le texte rejeté à une voix près',
      'Loi de programmation: le Sénat adopte le texte en première lecture',
    ],
    sentences: [
      'Le gouvernement a engagé sa responsabilité sur le projet de loi de finances, ouvrant la voie au dépôt d’une motion de censure dans les vingt-quatre heures.',
      'Les principaux syndicats appellent à une journée d’action interprofessionnelle, avec des perturbations attendues dans les transports et l’éducation.',
      'Le texte a été adopté par 289 voix contre 254, à l’issue de plus de quarante heures de débats dans l’hémicycle.',
      'L’opposition dénonce un passage en force et annonce la saisine du Conseil constitutionnel.',
      'La participation s’établit à 46,3 %, en recul de deux points par rapport au scrutin précédent.',
      'Le remaniement concerne quatre portefeuilles, dont l’Éducation nationale et les Comptes publics.',
      'Selon l’entourage du Premier ministre, aucune dissolution n’est envisagée à ce stade.',
      'Le budget 2026 prévoit un effort de vingt milliards d’euros, réparti entre baisse des dépenses et hausse des recettes.',
      'La réforme des retraites reste le principal point de friction entre la majorité et les organisations syndicales.',
    ],
  },
  {
    feed: 'Fil Monde',
    rubrique: 'International',
    types: ['depeche', 'depeche', 'article', 'transcription'],
    titles: [
      'Cessez-le-feu: les négociations reprennent sous médiation internationale',
      'Sommet du G20: les dirigeants divisés sur le financement climatique',
      'Élections législatives: la coalition sortante perd sa majorité',
      'Frontière: des milliers de déplacés fuient les combats',
      'Conseil de sécurité: une résolution bloquée par un veto',
      'Diplomatie: reprise des relations après quinze ans de rupture',
    ],
    sentences: [
      'Les pourparlers ont repris dans la capitale, sous l’égide de médiateurs internationaux, après trois semaines d’interruption.',
      'Le Conseil de sécurité de l’ONU s’est réuni en urgence à la demande de trois de ses membres permanents.',
      'Selon le Haut-Commissariat aux réfugiés, plus de quatre-vingt mille personnes ont fui la zone en une semaine.',
      'Les organisations humanitaires réclament l’ouverture de couloirs pour l’acheminement de l’aide alimentaire et médicale.',
      'Le scrutin s’est déroulé sans incident majeur, selon les observateurs déployés dans le pays.',
      'Un accord de cessez-le-feu de soixante-douze heures est entré en vigueur à minuit, heure locale.',
      'Le ministère des Affaires étrangères a convoqué l’ambassadeur pour protester contre ces déclarations.',
      'Le cessez-le-feu, s’il tient, doit permettre l’ouverture de négociations sur le statut des zones contestées.',
      'Le sommet du G20 s’est achevé sans communiqué commun, faute d’accord sur le financement climatique.',
    ],
  },
  {
    feed: 'Fil Éco',
    rubrique: 'Économie',
    types: ['depeche', 'depeche', 'article'],
    titles: [
      'Inflation: la hausse des prix ralentit à 2,1 % sur un an',
      'Banque centrale: statu quo sur les taux directeurs',
      'Emploi: le chômage stable au troisième trimestre',
      'Énergie: les tarifs réglementés révisés au 1er février',
      'Industrie: un plan social annoncé sur trois sites',
      'Croissance: la prévision annuelle revue à la baisse',
    ],
    sentences: [
      'L’indice des prix à la consommation progresse de 2,1 % sur un an, après 2,4 % le mois précédent, selon l’institut statistique.',
      'La banque centrale a maintenu ses taux directeurs inchangés, invoquant la persistance des tensions sur les salaires.',
      'Le taux de chômage s’établit à 7,3 % de la population active, un niveau quasi stable par rapport au trimestre précédent.',
      'Les marchés ont clôturé en léger repli, dans un volume d’échanges inférieur à la moyenne des trente dernières séances.',
      'Le groupe annonce la suppression de six cent quarante postes, concentrée sur trois sites de production.',
      'La prévision de croissance est ramenée à 0,9 % pour l’exercice, contre 1,2 % en début d’année.',
      'Les tarifs réglementés de l’électricité seront révisés au 1er février, après avis de la commission de régulation.',
      'L’inflation reste supérieure à la cible de 2 % fixée par la banque centrale, portée par les services et l’alimentation.',
      'L’emploi industriel recule pour le troisième trimestre consécutif, malgré la reprise des carnets de commandes.',
    ],
  },
  {
    feed: 'Fil Sport',
    rubrique: 'Sport',
    types: ['depeche', 'depeche', 'article'],
    titles: [
      'Jeux olympiques: le calendrier des épreuves dévoilé',
      'Football: le club se qualifie au terme des prolongations',
      'Cyclisme: victoire au sprint sur la troisième étape',
      'Tennis: forfait de la tête de série avant les quarts',
      'Rugby: le sélectionneur annonce une liste de trente-quatre joueurs',
      'Athlétisme: record national battu sur 1 500 mètres',
    ],
    sentences: [
      'L’équipe s’est imposée au terme des prolongations, après avoir égalisé à la dernière minute du temps réglementaire.',
      'Le coureur a réglé le sprint massif devant un peloton groupé et s’empare du maillot de leader.',
      'Le sélectionneur a retenu trente-quatre joueurs pour la préparation, dont cinq novices.',
      'La rencontre a été suivie par plus de soixante mille spectateurs, guichets fermés.',
      'L’athlète a amélioré le record national de plus d’une seconde, en 3 min 29 s 84.',
      'Le forfait a été annoncé à la veille des quarts de finale, en raison d’une blessure à la cuisse.',
      'Le calendrier des épreuves a été publié à cent jours de la cérémonie d’ouverture.',
      'Les Jeux olympiques débuteront dans cent jours, avec trente-deux sports au programme et douze mille athlètes attendus.',
      'Le club se qualifie pour les quarts de finale et affrontera le vainqueur de l’autre demi-finale.',
    ],
  },
  {
    feed: 'Fil France',
    rubrique: 'Culture',
    types: ['depeche', 'article', 'transcription'],
    titles: [
      'Festival: le jury dévoile son palmarès',
      'Cinéma: près de deux millions d’entrées en une semaine',
      'Littérature: le prix attribué à un premier roman',
      'Musée: une rétrospective inédite annoncée pour l’automne',
      'Musique: la tournée prolongée de douze dates',
      'Patrimoine: réouverture après quatre ans de travaux',
    ],
    sentences: [
      'Le jury a récompensé un premier long-métrage, salué par la critique lors de sa présentation en séance de nuit.',
      'Le film a réuni près de deux millions de spectateurs en une semaine d’exploitation.',
      'Le prix a été attribué au quatrième tour de scrutin, par six voix contre quatre.',
      'La rétrospective réunira plus de deux cents œuvres, dont une trentaine jamais montrées au public.',
      'La tournée est prolongée de douze dates supplémentaires, le premier calendrier ayant été complet en quelques heures.',
      'Le monument rouvre au public après quatre ans de travaux de restauration.',
      'La programmation fait une place inhabituelle aux premières œuvres et aux compagnies indépendantes.',
      'Le festival a présenté vingt-deux films en compétition officielle, dont sept premiers longs-métrages.',
      'Le prix littéraire distingue un roman consacré à la mémoire ouvrière d’une vallée industrielle.',
    ],
  },
  {
    feed: 'Fil Monde',
    rubrique: 'Sciences & Santé',
    types: ['depeche', 'article'],
    titles: [
      'Santé publique: campagne de vaccination avancée d’un mois',
      'Recherche: des résultats prometteurs en essai clinique',
      'Spatial: lancement reporté pour raisons météorologiques',
      'Épidémiologie: la surveillance renforcée dans trois régions',
      'Étude: un lien établi entre exposition et prévalence',
      'Antibiorésistance: l’agence alerte sur la hausse des cas',
    ],
    sentences: [
      'L’essai clinique de phase 3 a porté sur plus de quatre mille participants répartis dans onze pays.',
      'L’agence sanitaire recommande d’avancer d’un mois le début de la campagne de vaccination.',
      'Le lancement a été reporté de quarante-huit heures en raison des conditions météorologiques.',
      'Les auteurs de l’étude appellent à la prudence et soulignent les limites méthodologiques de leurs travaux.',
      'La surveillance épidémiologique est renforcée dans trois régions, où l’incidence progresse.',
      'L’Organisation mondiale de la santé a publié de nouvelles recommandations à destination des soignants.',
      'Les résultats devront être confirmés par une étude indépendante avant toute mise sur le marché.',
      'La campagne de vaccination cible en priorité les personnes de plus de soixante-cinq ans et les patients immunodéprimés.',
      'L’essai a été interrompu pour un tiers des participants, en raison d’effets indésirables modérés.',
    ],
  },
  {
    feed: 'Fil Monde',
    rubrique: 'Climat & Environnement',
    types: ['depeche', 'article'],
    titles: [
      'Climat: une année parmi les plus chaudes jamais mesurées',
      'COP: un accord a minima après deux nuits de négociation',
      'Sécheresse: restrictions d’eau étendues à douze départements',
      'Biodiversité: le déclin se poursuit selon un rapport',
      'Incendies: plus de quinze mille hectares parcourus',
      'Énergies renouvelables: la part dans le mix électrique progresse',
    ],
    sentences: [
      'L’année écoulée figure parmi les plus chaudes jamais enregistrées depuis le début des relevés.',
      'Le texte final, adopté après deux nuits de négociation, ne mentionne aucun calendrier contraignant.',
      'Les restrictions d’usage de l’eau sont étendues à douze départements placés en alerte renforcée.',
      'Le rapport documente un déclin continu des populations d’espèces suivies depuis cinquante ans.',
      'Les incendies ont parcouru plus de quinze mille hectares et mobilisé deux mille pompiers.',
      'La part des énergies renouvelables dans le mix électrique atteint un niveau inédit.',
      'Les négociateurs se retrouveront l’an prochain pour fixer les modalités de financement.',
      'Le climat mondial se réchauffe plus vite que ne le prévoyaient les projections publiées il y a dix ans.',
      'La COP a réuni près de deux cents délégations, sans parvenir à un calendrier de sortie des énergies fossiles.',
    ],
  },
  {
    feed: 'AFP Factuel',
    rubrique: 'Vérification',
    types: ['article', 'note'],
    titles: [
      'Non, cette publication virale ne concerne pas les inondations de la semaine dernière',
      'Attention à ce graphique trompeur sur les prix de l’énergie',
      'Cette citation attribuée à un responsable est inventée',
      'Ce document présenté comme officiel est un faux',
      'Non, ce chiffre sur la démographie ne provient pas de l’institut statistique',
      'Ce texte de loi n’a jamais été déposé au Parlement',
    ],
    sentences: [
      'La publication a été partagée plus de quarante mille fois avant d’être supprimée par son auteur.',
      'Contactée par l’AFP, l’institution concernée dément formellement avoir publié ce document.',
      'Le graphique tronque l’axe des ordonnées, ce qui exagère visuellement l’ampleur de la hausse.',
      'La citation n’apparaît dans aucune des archives consultées, ni dans les comptes rendus officiels.',
      'La recherche dans les bases documentaires permet de retrouver la source d’origine, publiée plusieurs années auparavant.',
      'Le chiffre avancé ne correspond à aucune publication de l’institut statistique, qui confirme ne pas en être l’auteur.',
      'Aucun texte portant ce numéro n’a été déposé au Parlement, selon le registre officiel des dépôts.',
      'La vérification s’appuie sur les archives de l’agence, les registres publics et les réponses des institutions concernées.',
      'Cette affirmation, largement relayée sur les réseaux sociaux, est trompeuse : les données citées ne disent pas cela.',
    ],
  },
  {
    feed: 'Fil France',
    rubrique: 'Société & Justice',
    types: ['depeche', 'depeche', 'article'],
    titles: [
      'Procès: le verdict attendu en fin de semaine',
      'Éducation: la réforme du lycée entre en vigueur à la rentrée',
      'Transports: grève reconduite pour vingt-quatre heures',
      'Logement: les demandes en hausse dans les grandes agglomérations',
      'Sécurité routière: la mortalité en baisse sur un an',
      'Immigration: le décret d’application publié au Journal officiel',
    ],
    sentences: [
      'Le tribunal a mis sa décision en délibéré : le verdict est attendu en fin de semaine.',
      'La grève est reconduite pour vingt-quatre heures, avec un trafic assuré à un train sur trois.',
      'Le décret d’application a été publié au Journal officiel, huit mois après l’adoption de la loi.',
      'La mortalité routière recule de 4 % sur un an, selon les chiffres provisoires de l’observatoire.',
      'La réforme entrera en vigueur à la rentrée, avec de nouveaux horaires en classe de seconde.',
      'Les associations dénoncent des délais d’instruction qui s’allongent dans les grandes agglomérations.',
      'L’audience a été renvoyée à une date ultérieure, à la demande de la défense.',
      'Le procès s’est ouvert devant la cour d’assises, en présence de plus de cent parties civiles.',
      'La grève dans les transports entre dans sa cinquième journée, avec un trafic très perturbé aux heures de pointe.',
    ],
  },
  {
    feed: 'Fil Éco',
    rubrique: 'Médias & Technologie',
    types: ['depeche', 'article'],
    titles: [
      'Intelligence artificielle: la régulation européenne entre en application',
      'Plateformes: obligation de signaler les contenus générés',
      'Presse: accord sur les droits voisins avec un moteur de recherche',
      'Cybersécurité: une attaque paralyse un opérateur régional',
      'Audiovisuel: fusion validée sous conditions',
      'Données personnelles: sanction record prononcée par le régulateur',
    ],
    sentences: [
      'Le règlement européen sur l’intelligence artificielle entre en application par étapes jusqu’en 2027.',
      'Les plateformes devront signaler de manière visible les contenus générés par intelligence artificielle.',
      'L’accord porte sur la rémunération des droits voisins pour la reprise de contenus de presse.',
      'L’attaque par rançongiciel a interrompu les services d’un opérateur régional pendant plus de trente heures.',
      'Le régulateur a prononcé une sanction record pour manquement à la protection des données personnelles.',
      'La fusion est validée sous conditions, avec des engagements de cession sur trois marchés.',
      'Les éditeurs réclament une répartition plus transparente des revenus issus de la reprise de leurs contenus.',
      'L’intelligence artificielle générative bouleverse les rédactions, qui encadrent son usage par des chartes internes.',
      'La cybersécurité devient un poste budgétaire prioritaire pour les opérateurs de services essentiels.',
    ],
  },
  {
    feed: 'Documentation rédaction',
    rubrique: 'Règles & procédures',
    types: ['note', 'note', 'transcription'],
    titles: [
      'Charte déontologique de l’agence',
      'Manuel de style et règles d’écriture des dépêches',
      'Protocole de couverture en zone de conflit',
      'Procédure de correction et de retrait d’une dépêche',
      'Guide de vérification des sources et des contenus',
      'Grille de priorités et niveaux d’urgence',
    ],
    sentences: [
      'Toute information doit être confirmée par au moins deux sources indépendantes avant publication.',
      'La correction d’une dépêche fait l’objet d’un message signalé, reprenant le texte initial et l’élément rectifié.',
      'Le titre d’une dépêche ne dépasse pas quatre-vingts caractères et ne comporte aucune abréviation non explicitée.',
      'Les niveaux d’urgence vont du flash à la dépêche de contexte, avec des délais de traitement associés.',
      'En zone de conflit, tout déplacement fait l’objet d’une analyse de risque validée par le desk et la sécurité.',
      'Les contenus soumis par des tiers sont vérifiés avant toute reprise, y compris lorsqu’ils émanent d’une source institutionnelle.',
      'La signature comporte le nom du journaliste, le bureau d’origine et l’heure de transmission.',
      'La charte déontologique rappelle que l’agence ne publie pas une information qu’elle n’a pas pu vérifier elle-même.',
      'Le manuel de style précise la structure d’une dépêche : titre, lead, corps, contexte et signature.',
    ],
  },
]

const BUREAUX = [
  'Paris',
  'Bruxelles',
  'Londres',
  'Berlin',
  'Genève',
  'Washington',
  'New York',
  'Nairobi',
  'Le Caire',
  'Pékin',
  'New Delhi',
  'Rio de Janeiro',
]

const JOURNALISTES = [
  'Camille Fournier',
  'Léa Bertrand',
  'Nicolas Meyer',
  'Sofia Ramos',
  'Julien Moreau',
  'Amina Cherif',
  'Thomas Weber',
  'Claire Dubois',
  'Marc Lemoine',
  'Inès Haddad',
  'Paul Rivière',
  'Nadia Belkacem',
]

const PREFIXES = [
  '',
  '',
  '',
  '',
  '',
  'URGENT: ',
  'FLASH: ',
  'PAPIER GÉNÉRAL: ',
  'ANALYSE: ',
  'REPORTAGE: ',
  'ENTRETIEN: ',
]

/** Suffixes des documents internes : pas de slug de fil d’agence. */
const DOC_SUFFIXES = ['', '', ' — mise à jour', ' — version 2026', ' — annexe', ' — synthèse']

const SUFFIXES = [
  '',
  '',
  ' — actualisé',
  ' — 2e lead',
  ' — encadré',
  ' — repères',
  ' — réactions',
  ' — contexte',
]

/** Formules de rédaction communes à tous les desks, pour étoffer les documents. */
const FILLERS = [
  'Aucune réaction officielle n’avait été publiée dans l’immédiat.',
  'Plusieurs sources concordantes ont confirmé cette information à l’AFP.',
  'Les acteurs concernés n’ont pas souhaité commenter à ce stade.',
  'Un point d’étape est attendu dans les prochaines semaines.',
  'Les chiffres définitifs seront publiés le mois prochain.',
  'Des vérifications complémentaires sont en cours auprès des parties prenantes.',
  'Le dossier doit encore franchir plusieurs étapes avant d’être définitivement clos.',
  'Cette annonce intervient dans un calendrier déjà chargé.',
  'L’agence poursuit la couverture de cet événement.',
  'Une mise à jour de cette dépêche est prévue en fin de journée.',
]

export function normalize(text: string): string {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[\u2019']/g, ' ')
}

export interface CorpusDoc extends DocumentMeta {
  /** Texte complet, découpé en paragraphes. */
  paragraphs: string[]
  /** Les paragraphes réunis : sert au scoring et à l’extraction d’extraits. */
  body: string
  /** Titre + corps normalisés, pré-calculés pour la recherche. */
  haystack: string
}

function buildCorpus(): CorpusDoc[] {
  const random = makeRandom(20260831)
  const docs: CorpusDoc[] = []
  const now = Date.UTC(2026, 7, 31)

  DESKS.forEach((desk, deskIndex) => {
    desk.titles.forEach((baseTitle, titleIndex) => {
      const variantCount = 10 + Math.floor(random() * 7)
      const seenTitles = new Set<string>()
      // Les slugs d’agence (URGENT, FLASH…) ne s’appliquent qu’aux fils d’actualité.
      const isWire = desk.feed !== 'Documentation rédaction' && desk.feed !== 'AFP Factuel'
      for (let v = 0; v < variantCount; v += 1) {
        const title = isWire
          ? PREFIXES[Math.floor(random() * PREFIXES.length)] +
            baseTitle +
            SUFFIXES[Math.floor(random() * SUFFIXES.length)]
          : baseTitle + DOC_SUFFIXES[Math.floor(random() * DOC_SUFFIXES.length)]
        if (seenTitles.has(title)) continue
        seenTitles.add(title)
        const type = desk.types[Math.floor(random() * desk.types.length)]
        const bureau = BUREAUX[Math.floor(random() * BUREAUX.length)]
        const author = JOURNALISTES[Math.floor(random() * JOURNALISTES.length)]
        const ageDays = Math.floor(random() ** 2 * 1200)
        const publishedAt = new Date(now - ageDays * 86400000 - Math.floor(random() * 86400000)).toISOString()

        const pool = [...desk.sentences]
        const sentences: string[] = []
        const sentenceCount = 5 + Math.floor(random() * 4)
        for (let s = 0; s < sentenceCount && pool.length > 0; s += 1) {
          sentences.push(pool.splice(Math.floor(random() * pool.length), 1)[0])
        }

        const fillerPool = [...FILLERS]
        const takeFiller = () => fillerPool.splice(Math.floor(random() * fillerPool.length), 1)[0]

        // Un paragraphe = deux phrases, la matière du desk d’abord, le liant ensuite.
        const paragraphs: string[] = []
        let cursor = 0
        while (cursor < sentences.length) {
          const chunk = sentences.slice(cursor, cursor + 2)
          if (chunk.length === 1) chunk.push(takeFiller())
          paragraphs.push(chunk.join(' '))
          cursor += 2
        }
        paragraphs.push([takeFiller(), takeFiller()].join(' '))

        const body = paragraphs.join('\n\n')
        const id = `doc-${deskIndex}-${titleIndex}-${v}`

        docs.push({
          id,
          title,
          path: [desk.feed, desk.rubrique, String(new Date(publishedAt).getUTCFullYear())],
          url: `#/document/${id}`,
          feed: desk.feed,
          type,
          bureau,
          author,
          publishedAt,
          words: body.trim().split(/\s+/).length,
          paragraphs,
          body,
          haystack: normalize(`${title} ${desk.rubrique} ${body}`),
        })
      }
    })
  })

  return docs
}

export const CORPUS: CorpusDoc[] = buildCorpus()

/** Taille annoncée de l’index côté produit ; le corpus local n’en est qu’un échantillon. */
export const INDEX_SIZE = 12_480_000
