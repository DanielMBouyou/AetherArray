# Backlog initial

- Statut : à transformer en issues GitHub à la création du dépôt
- Dernière revue : 2026-08-21

## Fil simulation, démarrage immédiat

| # | Titre | Type | Note |
| --- | --- | --- | --- |
| 1 | Implémenter le facteur de réseau et le vérifier sur les cas théoriques | experience | fondation de tout le fil |
| 2 | Ajouter injection de défauts, couplage et bruit | experience | permet de connaître la vérité |
| 3 | Reproduire l'effet statistique des erreurs de phase | experience | valide le simulateur contre la théorie |
| 4 | Implémenter la calibration voie par voie | experience | méthode de base |
| 5 | Implémenter la méthode par rotation de phase | experience | ne demande que des mesures de puissance |
| 6 | Implémenter l'inversion régularisée | experience | méthode complète |
| 7 | Comparer les méthodes à nombre de mesures compté | experience | résultat théorique principal |
| 8 | Étudier la sensibilité au bruit | experience | dimensionne les campagnes réelles |

## Fil matériel, bloquant

| # | Titre | Type | Note |
| --- | --- | --- | --- |
| 9 | Auditer les instruments disponibles | etude | conditionne tout |
| 10 | Vérifier la disponibilité d'un fenêtrage temporel sur l'analyseur | etude | pourrait résoudre le problème des échos |
| 11 | Caractériser les réflexions de l'environnement | experience | décide de la stratégie de mesure |
| 12 | Mesurer la reproductibilité d'une mesure de puissance | experience | plancher d'incertitude |
| 13 | Décider de la nature des ondes, RF ou acoustique | decision | dépend de 11 et 12 |
| 14 | Décider de la fréquence de travail | decision | dépend de 9 et 13 |

## Conception

| # | Titre | Type | Note |
| --- | --- | --- | --- |
| 15 | Comparer les architectures de formation de faisceau | etude | analogique, numérique, commutation |
| 16 | Chercher et chiffrer les composants de déphasage | etude | coût par voie |
| 17 | Décider de l'architecture | decision | détermine le rôle du FPGA |
| 18 | Concevoir les antennes | etude | reproductibilité entre éléments plus importante que performance |
| 19 | Réaliser un réseau à deux éléments | experience | premier système réel |
| 20 | Concevoir un positionneur angulaire | etude | utile aussi à NeuralRFIC |

## Mesure et validation

| # | Titre | Type | Note |
| --- | --- | --- | --- |
| 21 | Mesurer l'effet d'une erreur de câble connue | experience | démonstration la plus parlante du projet |
| 22 | Mesurer le diagramme non calibré | experience | état de départ |
| 23 | Appliquer une première calibration réelle | experience | résultat principal |
| 24 | Mesurer le couplage entre éléments | experience | valide ou invalide l'hypothèse de matrice diagonale |
| 25 | Mesurer la durée de validité d'une calibration | experience | demande du temps calendaire, à lancer tôt |

## Méthodes avancées

| # | Titre | Type | Note |
| --- | --- | --- | --- |
| 26 | Étudier l'optimisation bayésienne | etude | réduction du nombre de mesures |
| 27 | L'appliquer et mesurer le gain réel | experience | comparaison à budget de mesures égal |
| 28 | Décider si une méthode apprise est poursuivie | decision | dépend de 27 |

## Infrastructure

| # | Titre | Type | Note |
| --- | --- | --- | --- |
| 29 | Automatiser l'acquisition et l'archivage | etude | commun avec NeuralRFIC |
| 30 | Décider de la licence | decision | code, mesures et dessins de carte diffèrent |
| 31 | Organiser le partage de l'analyseur de réseau avec NeuralRFIC | decision | ressource unique |
