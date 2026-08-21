# Feuille de route

- Statut : proposition, révisable après chaque phase
- Dernière revue : 2026-08-21

## Phase 0 : théorie et simulateur

- [ ] Fondamentaux lus, équations écrites correctement
- [ ] Simulateur de réseau implémenté et vérifié sur les cas théoriques
- [ ] Défauts, couplage et bruit injectables
- [ ] Effet statistique des erreurs reproduit en simulation

**Sortie** : on dispose d'un banc virtuel où la vérité est connue.

## Phase 1 : méthodes de calibration en simulation

- [ ] Méthodes classiques implémentées
- [ ] Comparaison à nombre de mesures compté
- [ ] Sensibilité au bruit caractérisée
- [ ] Courbes qualité contre nombre de mesures produites

**Sortie** : le résultat théorique du projet existe, sans matériel.

## Phase 2 : environnement de mesure

- [ ] Instruments audités
- [ ] Réflexions de l'environnement caractérisées
- [ ] Reproductibilité de mesure chiffrée
- [ ] Stratégie de mesure décidée

**Sortie** : on sait si et comment on peut mesurer un diagramme.

## Phase 3 : premier réseau réel

- [ ] Architecture et fréquence choisies
- [ ] Réseau à deux éléments réalisé
- [ ] Effet d'une erreur de câble connue mesuré et conforme au calcul
- [ ] Diagramme non calibré mesuré

**Sortie** : la démonstration du problème existe, avec des mesures.

## Phase 4 : calibration réelle

- [ ] Première méthode de calibration appliquée au réseau réel
- [ ] Amélioration mesurée sur le diagramme
- [ ] Comparaison de plusieurs méthodes, mesures comptées
- [ ] Confrontation avec les prédictions de la phase 1

**Sortie** : le résultat principal du projet.

## Phase 5 : extension et robustesse

- [ ] Réseau à quatre éléments
- [ ] Couplage mesuré et pris en compte
- [ ] Durée de validité d'une calibration mesurée
- [ ] Sensibilité thermique évaluée

## Phase 6 : méthodes avancées

Conditionnelle.

- [ ] Optimisation bayésienne appliquée à la réduction du nombre de mesures
- [ ] Gain chiffré, ou absence de gain documentée
- [ ] Étude de la prédiction de dérive

## Points de sortie anticipée

| Arrêt après | Ce qui reste publiable |
| --- | --- |
| Phase 1 | une comparaison rigoureuse des méthodes de calibration en simulation |
| Phase 3 | une démonstration mesurée de l'écart entre théorie et réalité |
| Phase 4 | le résultat complet du projet |

## Décision structurante à prendre tôt

La nature du réseau, radiofréquence ou acoustique, doit être tranchée à la fin de
la phase 2, en fonction de ce que l'environnement de mesure permet réellement. Ce
choix change le coût, le calendrier et la présentation du projet, mais pas son
contenu scientifique.
