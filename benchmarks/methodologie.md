# Méthodologie de comparaison des méthodes de calibration

- Statut : en cours
- Dernière revue : 2026-08-21

---

## 1. Le problème de fond

Sur un réseau réel, on ne connaît pas la vérité. On ne peut donc pas dire si une
méthode de calibration a trouvé les bons paramètres, seulement si le résultat
final est meilleur.

D'où une organisation en deux temps :

| Temps | Objet | Ce qu'on peut mesurer |
| --- | --- | --- |
| Simulation | réseau virtuel avec défauts connus | l'erreur d'estimation, donc la justesse de la méthode |
| Réel | réseau physique | l'amélioration du diagramme, donc l'efficacité pratique |

Les deux sont nécessaires. La simulation dit si la méthode est correcte, le réel
dit si elle survit au bruit et aux imperfections non modélisées.

## 2. Le banc de simulation

Un simulateur de réseau avec défauts injectés est un outil peu coûteux et très
rentable. Il permet de comparer toutes les méthodes avant même d'avoir du matériel.

Il doit inclure :

| Élément | Pourquoi |
| --- | --- |
| Erreurs de gain et de phase par voie, tirées au hasard | c'est le défaut principal |
| Couplage entre éléments voisins | pour tester les méthodes qui l'ignorent |
| Bruit de mesure, avec un niveau réglable | pour tester la robustesse |
| Quantification des commandes | si des déphaseurs à pas discrets sont utilisés |
| Dérive lente | pour tester la durée de validité |

Le point clé est que les défauts sont **connus**, donc l'erreur d'estimation est
mesurable exactement. C'est impossible sur un réseau réel.

## 3. Protocole de comparaison

Pour chaque méthode de calibration :

1. Fixer un tirage de défauts, identique pour toutes les méthodes.
2. Lancer la méthode, en comptant le nombre de mesures qu'elle consomme.
3. Relever l'erreur d'estimation, en simulation, ou la qualité du diagramme
   obtenu, sur le réel.
4. Répéter sur plusieurs tirages de défauts et plusieurs niveaux de bruit.
5. Tracer la qualité obtenue en fonction du nombre de mesures consommées.

La courbe du point 5 est le résultat principal du projet. Elle répond à la vraie
question : combien de mesures faut-il, et que gagne-t-on à en faire plus.

## 4. Le nombre de mesures est la ressource comptée

Contrairement aux autres projets du laboratoire, la ressource rare ici n'est pas le
temps de calcul mais le **nombre de mesures physiques**. Une mesure demande un
déplacement mécanique, une stabilisation, une acquisition, et elle est bruitée.

C'est ce qui rend l'optimisation bayésienne pertinente : elle est justement conçue
pour les situations où chaque évaluation coûte cher.

Toute méthode sera donc caractérisée par deux nombres au moins : la qualité
atteinte, et le nombre de mesures consommées pour l'atteindre.

## 5. Protocole de mesure réelle

| Étape | Contenu | Pourquoi |
| --- | --- | --- |
| 1 | Vérification du montage, longueurs de câbles notées | les câbles font partie du système |
| 2 | Mesure de référence sur une voie seule | permet de détecter une dérive globale |
| 3 | Mesure du diagramme non calibré | l'état de départ |
| 4 | Application de la méthode de calibration | en comptant les mesures |
| 5 | Mesure du diagramme calibré | le résultat |
| 6 | Nouvelle mesure de référence | détecte une dérive pendant la campagne |
| 7 | Répétition à quelques heures d'intervalle | mesure la durée de validité |

L'étape 7 est celle qui produit le résultat le plus original, et elle ne coûte que
de la patience.

## 6. Précautions spécifiques

| Précaution | Raison |
| --- | --- |
| Ne pas toucher au montage entre les mesures comparées | un connecteur resserré change tout |
| Noter la température ambiante | elle explique une partie des dérives |
| Éloigner l'opérateur pendant la mesure | le corps humain réfléchit et absorbe |
| Répéter chaque point de mesure | pour estimer le bruit |
| Mesurer un cas connu au début et à la fin | pour détecter une dérive du banc |

La troisième ligne n'est pas une plaisanterie : à ces longueurs d'onde, une
personne debout à côté du montage modifie le diagramme de façon mesurable.

## 7. Ce qu'on compare

| Configuration | Rôle |
| --- | --- |
| Simulation idéale | ce que la théorie prévoit |
| Réel non calibré | l'état de départ, souvent spectaculairement mauvais |
| Calibration voie par voie | méthode de base |
| Calibration par rotation de phase | méthode classique sans mesure de phase |
| Inversion régularisée | méthode complète |
| Optimisation directe | sans estimer la matrice |
| Optimisation bayésienne | pour réduire le nombre de mesures |
| Méthode apprise éventuelle | si elle apporte quelque chose |

## 8. Ce qu'on ne fera pas

- Pas de comparaison sans compter le nombre de mesures.
- Pas de conclusion sur un seul tirage de défauts.
- Pas de diagramme publié sans indiquer les conditions de mesure et
  l'environnement.
- Pas de résultat de simulation présenté comme une mesure.
