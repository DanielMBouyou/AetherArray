# Cadrage du projet AetherArray

- Statut : en cours
- Dernière revue : 2026-08-21

## 1. Quel problème veut-on résoudre

Construire un réseau d'antennes commandé électroniquement, mesurer l'écart entre
son comportement réel et son comportement théorique, et déterminer quelle méthode
de calibration corrige cet écart au meilleur coût, où le coût se mesure surtout en
nombre de mesures physiques.

## 2. Pourquoi ce problème est intéressant

- Il met en évidence de façon spectaculaire l'écart entre un modèle propre et la
  réalité physique. Un centimètre de câble suffit à ruiner un diagramme.
- Il combine électronique, RF, traitement du signal, optimisation et métrologie
  dans un seul objet.
- Il pose un vrai problème inverse : retrouver des paramètres cachés à partir de
  mesures indirectes et bruitées.
- La question du nombre de mesures nécessaires est un point où une méthode
  d'optimisation ou d'apprentissage peut réellement apporter quelque chose, et où
  ce gain est directement mesurable.
- Les compétences visées sont recherchées dans les domaines du radar, des
  communications et de l'instrumentation.

## 3. Formulation

Le système réel est décrit par :

```
y = H · x
```

`x` est le vecteur des commandes appliquées aux voies, `y` ce qui sort réellement,
et `H` une matrice complexe contenant les erreurs de gain, de phase et les
couplages.

Le problème de calibration consiste à estimer `H` à partir d'un nombre limité de
mesures, puis à en déduire la commande corrigée. Le problème d'optimisation
consiste à trouver la commande qui donne le diagramme le plus proche d'un
diagramme cible, ce qui n'est pas exactement la même chose et sera distingué.

Détail complet dans `docs/mathematics/formulation.md`.

## 4. Quelles solutions existent déjà

Voir `research/etat-de-l-art.md`. En résumé :

- Une littérature ancienne et solide sur les réseaux d'antennes, les diagrammes,
  le couplage mutuel et les erreurs de réalisation.
- Des méthodes de calibration éprouvées, dont certaines n'utilisent que des
  mesures de puissance.
- Des kits pédagogiques commerciaux de réseau à commande de phase, entièrement
  documentés, qui montrent une architecture réaliste.
- Une littérature récente appliquant l'optimisation bayésienne à la calibration et
  au réglage de systèmes coûteux à évaluer.

## 5. Quelles familles comparer

| Famille | Description | Coût en mesures |
| --- | --- | --- |
| Pas de calibration | on applique la théorie telle quelle | nul |
| Calibration voie par voie | on mesure chaque voie séparément | proportionnel au nombre de voies |
| Méthode par rotation de phase | on fait varier la phase d'une voie et on observe la puissance totale | plusieurs mesures par voie, mais sans mesure de phase |
| Inversion par moindres carrés | on estime la matrice complète | dépend du nombre de mesures |
| Moindres carrés régularisés | idem, avec contrainte de stabilité | idem |
| Optimisation directe du diagramme | on cherche la commande qui donne le meilleur diagramme, sans passer par la matrice | nombreuses évaluations |
| Optimisation bayésienne | on choisit intelligemment la mesure suivante | conçue pour réduire le nombre de mesures |
| Méthode apprise | modèle prédictif de la dérive ou des paramètres manquants | dépend |

## 6. Quelles ressources avons-nous

Analyseur de réseau vectoriel, oscilloscope, générateur, cartes FPGA,
microcontrôleurs, PC. Détail et caractéristiques à établir dans
`docs/hardware/inventaire-et-besoins.md`. Le partage avec NeuralRFIC est direct.

## 7. Quelles ressources manquent

- Un moyen de mesurer un diagramme de rayonnement dans de bonnes conditions :
  absorbants, positionneur angulaire, environnement maîtrisé.
- Des déphaseurs commandables, sauf si l'on choisit une architecture numérique.
- Éventuellement plusieurs voies de réception cohérentes, si l'on fait de la
  formation de faisceau numérique.
- Des antennes, qui peuvent être fabriquées sur circuit imprimé.

## 8. Quels benchmarks

Voir `benchmarks/methodologie.md`. Principe : comparer les méthodes de calibration
sur le même réseau, avec les mêmes défauts, en comptant le nombre de mesures
consommées par chacune.

Point de méthode important : une grande partie de la comparaison peut se faire
**en simulation**, sur un réseau virtuel dont on connaît les défauts exactement.
C'est même la seule façon de savoir si une méthode retrouve la bonne réponse,
puisque sur un réseau réel on ne connaît pas la vérité.

## 9. Quelles métriques

Voir `benchmarks/metriques.md` : erreur de pointage, gain, niveau des lobes
secondaires, largeur du faisceau, nombre de mesures, temps de calibration,
robustesse au bruit et à la température, stabilité dans le temps.

## 10. Principales inconnues

1. La qualité de mesure atteignable dans l'environnement disponible.
2. La possibilité de mesurer la phase, ou seulement la puissance.
3. Le niveau réel des erreurs de voie dans un montage fait maison.
4. L'importance réelle du couplage entre éléments à l'espacement retenu.
5. Le nombre minimal de mesures pour une calibration acceptable.
6. La durée de validité d'une calibration.

## 11. Quelles expériences

Voir `experiments/plan.md`. Comme pour NeuralRFIC, le travail est organisé en deux
fils : un fil simulation qui peut démarrer immédiatement, et un fil matériel
contraint par les délais.

## 12. Le plus petit prototype crédible

Deux éléments seulement. Avec deux voies, on peut déjà mesurer un déphasage, faire
tourner un faisceau simple, observer l'effet d'une erreur de câble, et tester une
calibration. Le passage à quatre éléments n'ajoute pas de question nouvelle, il
ajoute de la résolution.

Commencer par deux voies réduit fortement le coût et le risque, et permet
d'atteindre un résultat mesurable très vite.

## 13. Étapes suivantes

Voir `ROADMAP.md`.

## 14. Ce qui peut être mutualisé

Voir `docs/mutualisation.md`. Le lien avec NeuralRFIC est fort : instruments,
calibration, automatisation, traitement des paramètres S, connectique,
fabrication de cartes. Le lien avec les projets FPGA est réel mais conditionnel :
il ne devient pertinent que si l'on choisit la formation de faisceau numérique.

## 15. Ce qui rendrait le projet irréalisable ou sans intérêt

- Si l'environnement de mesure ne permet pas de distinguer un diagramme des échos
  de la pièce, aucune conclusion sur le rayonnement n'est possible. Replis : mesure
  au contact voie par voie, mesure différentielle, ou passage à un réseau
  acoustique pour la partie algorithmique.
- Si les erreurs de voie se révèlent négligeables, il n'y a rien à calibrer. C'est
  peu probable, mais dans ce cas on peut en introduire volontairement et
  contrôlées, ce qui reste un sujet d'étude valable.
- Si le coût des composants dépasse le budget, l'architecture numérique ou
  acoustique devient la voie de repli.
- Si le projet se transforme en simple assemblage d'un kit du commerce, il perd son
  contenu. Le kit peut servir de référence, pas de finalité.

## Hors périmètre

- Conception d'un radar complet.
- Émission à forte puissance ou hors des bandes libres.
- Réseau à grand nombre d'éléments.
- Traitement d'antennes multi-utilisateurs.
