# Métriques

- Statut : en cours
- Dernière revue : 2026-08-21

---

## 1. Métriques de diagramme

| Métrique | Définition | Unité | Remarque |
| --- | --- | --- | --- |
| Erreur de pointage | écart entre la direction demandée et la direction du maximum observé | degrés | métrique la plus parlante |
| Gain dans la direction visée | puissance reçue par rapport à un élément seul | dB | mesure la qualité de la recombinaison |
| Niveau des lobes secondaires | rapport entre le plus haut lobe secondaire et le lobe principal | dB | souvent plus dégradé que le gain |
| Largeur du faisceau à mi-puissance | angle entre les points à -3 dB | degrés | doit correspondre à la théorie |
| Écart au diagramme cible | mesure globale de différence entre diagramme obtenu et diagramme visé | dB | métrique de synthèse |

L'erreur de pointage est la métrique à mettre en avant, parce qu'elle est
immédiatement compréhensible : le faisceau ne va pas là où on lui demande, et on
peut le montrer sur une figure.

## 2. Métriques d'estimation, en simulation seulement

| Métrique | Définition | Utilité |
| --- | --- | --- |
| Erreur sur les phases estimées | écart entre phases estimées et phases réellement injectées | mesure la justesse de la méthode |
| Erreur sur les gains estimés | idem pour les amplitudes | idem |
| Erreur résiduelle sur la matrice | norme de la différence entre matrice estimée et matrice réelle | vue globale |
| Nombre de conditionnement | mesure de la stabilité de l'inversion | prédit la sensibilité au bruit |

Ces métriques ne sont accessibles qu'en simulation, puisqu'elles demandent de
connaître la vérité. C'est précisément pour cela que le banc de simulation est
indispensable.

## 3. Métriques de coût

| Métrique | Unité | Pourquoi |
| --- | --- | --- |
| Nombre de mesures physiques | nombre | c'est la ressource rare de ce projet |
| Temps de calibration | minutes | inclut les déplacements mécaniques |
| Temps de calcul | secondes | généralement négligeable devant le reste |
| Nombre de positions angulaires nécessaires | nombre | conditionne le temps total |

Le rapport entre la première et la troisième ligne est frappant : une mesure prend
des secondes ou des minutes, le calcul associé prend des millisecondes. Optimiser
le calcul n'a aucun intérêt, optimiser le nombre de mesures en a beaucoup. C'est ce
déséquilibre qui oriente tout le projet.

## 4. Métriques de robustesse

| Métrique | Définition | Comment la mesurer |
| --- | --- | --- |
| Sensibilité au bruit | dégradation quand le bruit de mesure augmente | balayage en simulation, mesures répétées sur le réel |
| Stabilité dans le temps | dégradation du diagramme après quelques heures sans recalibrer | mesures répétées |
| Sensibilité thermique | variation en fonction de la température | mesures à plusieurs températures |
| Sensibilité au remontage | effet du démontage et remontage des câbles | mesures répétées après manipulation |

La dernière ligne mesure quelque chose d'important : si le simple fait de
débrancher et rebrancher un câble invalide la calibration, cela change complètement
l'usage pratique du système.

## 5. Tableau de résultats type

| Méthode | Nombre de mesures | Erreur de pointage | Gain | Lobes secondaires | Largeur de faisceau | Validité après quelques heures |
| --- | --- | --- | --- | --- | --- | --- |
| non calibré | 0 | à mesurer | à mesurer | à mesurer | à mesurer | sans objet |
| voie par voie | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer |
| rotation de phase | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer |
| inversion régularisée | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer |
| optimisation bayésienne | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer | à mesurer |

La première ligne est le témoin. Elle donne la mesure de ce que la calibration
apporte réellement, et c'est la plus facile à obtenir.

## 6. Ce qu'on ne fera pas

- Pas de métrique de diagramme annoncée sans les conditions de mesure.
- Pas de comparaison de méthodes sans le nombre de mesures consommées.
- Pas de conclusion sur un écart inférieur au bruit de mesure répétée.
- Pas de résultat de simulation présenté sans son étiquette.
