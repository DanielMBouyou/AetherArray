# Conventions du dépôt

Ce document fixe la manière dont le dépôt est organisé et écrit. Il est
volontairement court. Si une règle gêne le travail réel, on la change et on note
pourquoi dans `decisions/`.

## 1. Pourquoi cette arborescence

L'objectif est qu'un lecteur qui arrive sur le dépôt puisse répondre à une
question précise sans lire tout le reste.

| Dossier | Question à laquelle il répond |
| --- | --- |
| `README.md` | De quoi s'agit-il, et pourquoi c'est intéressant ? |
| `docs/cadrage.md` | Quel est le problème, quel est le périmètre, qu'est-ce qui est hors périmètre ? |
| `docs/incertitudes.md` | Qu'est-ce qui est certain, supposé, ou à vérifier ? |
| `research/` | Qu'existe-t-il déjà, et qu'est-ce qu'on doit lire ? |
| `docs/architecture/` | Quelles architectures sont possibles, et comment les départager ? |
| `docs/mathematics/` | Comment le problème s'écrit formellement ? |
| `benchmarks/` | Comment mesure-t-on, et avec quelles métriques ? |
| `experiments/` | Quelles manipulations concrètes sont prévues, dans quel ordre ? |
| `docs/hardware/` | Quel matériel est nécessaire, disponible, ou manquant ? |
| `docs/verification/` | Comment sait-on qu'un résultat est juste ? |
| `results/` | Qu'a-t-on réellement mesuré ? |
| `docs/references/` | Où trouver les sources et le vocabulaire ? |
| `decisions/` | Qu'a-t-on décidé, sur quelles preuves, et quand faut-il y revenir ? |

Deux points méritent une justification, parce qu'ils s'écartent d'une liste plate.

**`research/` est à la racine et non dans `docs/`.** Pendant cette phase, la
bibliographie n'est pas de la documentation d'accompagnement, c'est le travail
principal. La mettre au même niveau que `benchmarks/` et `experiments/` reflète
son poids réel.

**`experiments/` (le plan) et `results/` (les mesures) sont séparés.** Un plan
d'expérience est écrit une fois et révisé rarement. Les résultats s'accumulent,
grossissent, et sont parfois versionnés autrement (voir `results/README.md`).
Les mélanger rend l'historique git illisible.

## 2. État d'un document

Chaque document important commence par un bloc d'état :

```
Statut : brouillon | en cours | stable | périmé
Dernière revue : AAAA-MM-JJ
```

Un document `périmé` n'est pas supprimé. On garde la trace de ce qu'on croyait.

## 3. Marquage de la confiance

Dans tout le dépôt, trois marqueurs sont utilisés et n'ont pas le même sens :

- **[certain]** : vérifié par une source primaire (fiche technique, mesure faite
  ici, spécification officielle) et la source est citée.
- **[supposé]** : hypothèse de travail raisonnable, non vérifiée, utilisée pour
  avancer. Doit pouvoir être invalidée.
- **[à vérifier]** : question ouverte identifiée, avec si possible la méthode de
  vérification.

Dans les tableaux comparatifs, une case vide est interdite. On écrit `à mesurer`
ou `à vérifier`. Une fausse valeur est pire qu'une absence de valeur.

## 4. Nommage

- Fichiers et dossiers : minuscules, tirets simples, **sans accent** (portabilité
  entre systèmes de fichiers et entre outils). Le contenu, lui, est écrit en
  français normal.
- Décisions : `decisions/NNNN-titre-court.md`, numérotation continue, jamais réutilisée.
- Expériences : `EXP-NNN-titre-court`.
- Résultats : `results/EXP-NNN/` qui reprend l'identifiant de l'expérience.
- Fiches de veille : `research/fiches/NNN-nom-solution.md`.

## 5. Unités et notation

- Unités SI, préfixes explicites. Temps en ns, µs, ms.
- Les grandeurs logarithmiques portent leur référence : dBm, dBc, dB.
- Toute équation introduite dans un document doit être suivie d'une phrase qui dit
  ce que chaque symbole représente physiquement. Une équation sans explication est
  considérée comme un défaut de documentation.

## 6. Style d'écriture

- Phrases courtes. Pas de superlatif. Pas de vocabulaire promotionnel.
- On écrit ce qu'on a mesuré, pas ce qu'on espère mesurer.
- Le tiret cadratin est interdit dans tout le dépôt (problème d'encodage et de
  copier-coller entre outils). Utiliser virgule, parenthèse, deux points.
  `tools/check-docs.sh` vérifie ce point.
- Les nombres issus d'une documentation constructeur sont annoncés comme tels.
  "annoncé à 30 ns par le constructeur" et "mesuré à 30 ns ici" ne sont pas la
  même information.

## 7. Données

- Aucun fichier binaire lourd dans l'historique git tant qu'une politique n'est
  pas décidée (voir `results/README.md`).
- Aucune donnée sous licence restrictive, aucune clé, aucun jeton d'accès, aucun
  document constructeur soumis à un accord de confidentialité.
- Chaque jeu de données présent doit avoir un fichier `SOURCE.md` à côté, qui
  donne l'origine, la licence et la date de récupération.

## 8. Cycle de vie d'une question

```
question ouverte  ->  fiche de recherche  ->  expérience  ->  résultat  ->  décision
   (docs/)              (research/)          (experiments/)   (results/)   (decisions/)
```

Une décision qui ne s'appuie sur aucun résultat doit le dire explicitement, et
préciser sur quelle base elle est prise (contrainte de temps, de budget, de
matériel).

## 9. Rapport avec les autres dépôts du laboratoire

Ce dépôt est autonome : il se lit et s'utilise seul. Il fait partie d'un ensemble
de cinq projets qui partagent du matériel et des méthodes. Les éléments
mutualisables sont signalés dans `docs/mutualisation.md`. Aucune dépendance de
code vers un autre dépôt n'est autorisée tant qu'une bibliothèque commune n'a pas
été formellement décidée.
