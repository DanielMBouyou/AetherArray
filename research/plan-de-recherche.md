# Programme de recherche

- Statut : en cours
- Dernière revue : 2026-08-21

## Principe

Deux fils parallèles. Le fil simulation démarre immédiatement et produit le
résultat théorique. Le fil matériel, plus lent, produit la validation réelle.

## Lot 1 : fondamentaux et simulateur (fil simulation)

| Tâche | Livrable | Critère d'arrêt |
| --- | --- | --- |
| Lire les fondamentaux sur les réseaux d'antennes | fiches A1 et A2 | on écrit les équations sans erreur |
| Implémenter le facteur de réseau et le vérifier | simulateur testé | largeur de faisceau et lobes secondaires conformes à la théorie |
| Ajouter défauts, couplage et bruit | simulateur complet | défauts connus, donc erreur d'estimation mesurable |
| Étudier l'effet statistique des erreurs | fiche A9 | on sait prédire la perte de gain avant de mesurer |

## Lot 2 : méthodes de calibration (fil simulation)

| Tâche | Livrable | Critère d'arrêt |
| --- | --- | --- |
| Étudier la méthode par rotation de phase | fiche A6 | méthode comprise et implémentée |
| Étudier la calibration par le couplage | fiche A7 | on sait si elle est applicable ici |
| Implémenter les méthodes classiques | code testé | résultats corrects en simulation |
| Étudier la régularisation et le conditionnement | fiche A11 | on sait diagnostiquer une inversion instable |
| Comparer les méthodes en simulation | EXP-002 | courbes qualité contre nombre de mesures |

## Lot 3 : environnement de mesure (fil matériel, bloquant)

| Tâche | Livrable | Critère d'arrêt |
| --- | --- | --- |
| Auditer les instruments | inventaire rempli | on sait ce qu'on peut mesurer |
| Vérifier la disponibilité d'un fenêtrage temporel | note | on sait comment traiter les échos |
| Caractériser les réflexions de l'environnement | EXP-005 | plancher d'incertitude chiffré |
| Décider de la stratégie de mesure | fiche de décision | choix argumenté |

## Lot 4 : conception du réseau

| Tâche | Livrable | Critère d'arrêt |
| --- | --- | --- |
| Comparer les architectures | `docs/architecture/options.md` complété | quatre options chiffrées |
| Choisir la nature des ondes et la fréquence | fiche de décision | justifiée par les moyens de mesure |
| Étudier les composants de déphasage disponibles | comparatif avec prix | on connaît le coût par voie |
| Concevoir un réseau à deux éléments | schéma et dessin | premier système réalisable |

## Lot 5 : mesures et validation

| Tâche | Livrable | Critère d'arrêt |
| --- | --- | --- |
| Mesurer l'effet d'une erreur de câble connue | EXP-007 | accord entre calcul et mesure |
| Calibrer le réseau réel | EXP-008 | amélioration mesurée du diagramme |
| Étendre à quatre éléments | EXP-009 | couplage observable |
| Mesurer la durée de validité | EXP-010 | courbe de dégradation dans le temps |

## Lot 6 : méthodes avancées

Conditionnel aux résultats du lot 2.

| Tâche | Livrable | Critère d'arrêt |
| --- | --- | --- |
| Étudier l'optimisation bayésienne | fiche A13 | méthode comprise |
| L'appliquer à la réduction du nombre de mesures | résultats | gain chiffré, ou absence de gain |
| Étudier la prédiction de dérive | note | faisabilité évaluée |

## Compétences à acquérir

| Compétence | Niveau visé | Comment | Vérifiable par |
| --- | --- | --- | --- |
| Théorie des réseaux d'antennes | savoir prédire un diagramme | ouvrages de référence | simulateur conforme à la théorie |
| Mesure de diagramme | savoir mesurer proprement | pratique et protocole écrit | mesure reproductible |
| Problèmes inverses et régularisation | savoir diagnostiquer une inversion instable | littérature, simulation | conditionnement calculé et interprété |
| Optimisation sans gradient | savoir choisir et régler une méthode | littérature, essais | comparaison honnête avec une référence |
| Conception d'antennes imprimées | savoir concevoir et simuler | outils disponibles | adaptation mesurée conforme |
| Automatisation de banc de mesure | savoir piloter et archiver | commun avec NeuralRFIC | campagne automatisée |

## Critère d'arrêt de la phase d'étude

1. Le simulateur existe et est vérifié.
2. Les méthodes classiques sont comparées en simulation.
3. L'environnement de mesure est caractérisé, avec un plancher d'incertitude
   chiffré.
4. L'architecture du réseau est choisie et justifiée.
