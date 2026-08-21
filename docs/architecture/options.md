# Architectures candidates

- Statut : ouvert, aucun choix fait
- Dernière revue : 2026-08-21

---

## 1. Les trois façons de former un faisceau

| Approche | Principe | Matériel par voie | Souplesse | Coût |
| --- | --- | --- | --- | --- |
| Analogique | déphaseurs et atténuateurs sur le signal RF, une seule chaîne de conversion | un déphaseur, un atténuateur | un seul faisceau à la fois | modéré |
| Numérique | une chaîne de conversion complète par voie, tout se fait par le calcul | un convertisseur et un émetteur-récepteur | totale, plusieurs faisceaux simultanés | élevé |
| Hybride | sous-groupes analogiques, combinés numériquement | intermédiaire | intermédiaire | intermédiaire |

Conséquence directe pour ce projet : **le FPGA n'a d'intérêt que dans les
approches numérique ou hybride.** En analogique, un microcontrôleur suffit
largement à piloter des déphaseurs. Ce point doit être tranché consciemment, pas
subi.

## 2. Options de mise en oeuvre

### Option A : réseau analogique avec déphaseurs commandés

Des composants dédiés appliquent un déphasage réglable à chaque voie.

| Aspect | Évaluation |
| --- | --- |
| Complexité électronique | moyenne |
| Coût | dépend fortement des composants, à chiffrer |
| Réalisme | c'est l'architecture des systèmes réels |
| Problème de calibration | bien posé, et c'est le sujet |
| Rôle du FPGA | aucun, un microcontrôleur suffit |

### Option B : réseau numérique multi-voies

Chaque voie a sa propre chaîne de conversion, la formation de faisceau se fait par
le calcul.

| Aspect | Évaluation |
| --- | --- |
| Complexité | élevée, il faut synchroniser les voies |
| Coût | élevé |
| Souplesse | maximale |
| Problème de calibration | toujours présent, et plus riche |
| Rôle du FPGA | central, y compris pour la synchronisation |

Difficulté spécifique et intéressante : la cohérence entre voies. Deux récepteurs
séparés ont chacun leur oscillateur, et leur différence de phase dérive. Il faut
soit une horloge commune, soit une voie de référence. C'est un vrai problème
d'ingénierie, et il rejoint directement les compétences de synchronisation
développées dans muMarket.

### Option C : déphasage par commutation de lignes

On sélectionne des longueurs de ligne différentes pour créer des déphasages
discrets, par exemple par pas de 90 degrés.

| Aspect | Évaluation |
| --- | --- |
| Complexité | faible |
| Coût | faible |
| Précision | limitée par la quantification du déphasage |
| Intérêt pédagogique | fort, tout est visible et compréhensible |
| Limite | la quantification limite la précision de pointage |

La quantification de phase est un sujet en soi : avec des pas de 90 degrés,
l'erreur maximale est de 45 degrés, ce qui dégrade fortement le diagramme. Étudier
cet effet est instructif et peu coûteux.

### Option D : réseau acoustique

On transpose tout le problème à des ultrasons, autour de 40 kHz.

| Aspect | Évaluation |
| --- | --- |
| Coût | très faible |
| Complexité électronique | faible, le déphasage se fait numériquement à basse fréquence |
| Mesure | facile, avec un microphone et un déplacement mécanique |
| Physique | identique dans son principe, longueur d'onde d'environ 8,6 mm |
| Limite | ce ne sont pas des ondes électromagnétiques, il faut le dire clairement |

Cette option n'est pas un gadget. Toute la partie algorithmique, calibration,
optimisation et mesure de diagramme, est identique. Elle permettrait de produire
des résultats complets et validés très rapidement, puis de porter la méthode sur
un réseau RF.

Son défaut est de communication : un projet de réseau d'antennes qui n'utilise pas
d'antennes demande une explication. Cette explication est facile à donner si les
résultats sont bons.

### Option E : kit pédagogique du commerce

Un réseau à commande de phase déjà conçu, documenté et fonctionnel.

| Aspect | Évaluation |
| --- | --- |
| Coût | à vérifier, probablement significatif |
| Temps gagné | considérable |
| Apprentissage de la conception | faible |
| Intérêt | permet de se concentrer entièrement sur la calibration et les algorithmes |

À considérer honnêtement : si l'objectif principal est l'étude de la calibration,
partir d'un réseau qui fonctionne déjà n'est pas de la triche, c'est un choix de
périmètre. Le risque est de se retrouver à simplement suivre un tutoriel.

---

## 3. Matrice de comparaison

| Option | Coût | Délai | Difficulté de mesure | Richesse du problème de calibration | Rôle du FPGA | Risque |
| --- | --- | --- | --- | --- | --- | --- |
| A analogique | moyen | moyen | élevée | bonne | nul | moyen |
| B numérique | élevé | long | élevée | excellente | central | élevé |
| C commutation | faible | court | élevée | bonne, avec quantification | nul | faible |
| D acoustique | très faible | très court | faible | bonne | possible mais non nécessaire | très faible |
| E kit du commerce | à chiffrer | court | moyenne | bonne | nul | faible |

**Enchaînement suggéré, à discuter** : commencer par D pour valider les
algorithmes de calibration dans de bonnes conditions de mesure, puis passer à A ou
C sur deux voies, puis étendre. L'option B n'a de sens que si la formation de
faisceau numérique devient un objectif explicite.

Cet enchaînement a la même propriété que celui de NeuralRFIC : chaque étape produit
un résultat utilisable même si la suivante n'a jamais lieu.

---

## 4. Options d'antenne

| Type | Fabrication | Bande | Remarque |
| --- | --- | --- | --- |
| Antenne imprimée sur circuit | à commander | étroite | facile à reproduire à l'identique, ce qui compte pour un réseau |
| Antenne filaire | faite main | moyenne | irrégularités entre éléments, ce qui est justement ce qu'on étudie |
| Antenne du commerce | achat | selon modèle | reproductibilité correcte, coût par élément |

Point intéressant : la reproductibilité entre éléments est un critère plus
important que la performance de chaque élément. Un réseau de quatre antennes
médiocres mais identiques se calibre mieux qu'un réseau de quatre bonnes antennes
toutes différentes.

---

## 5. Décisions à prendre plus tard

| Décision | Ce qui manque pour trancher | Conséquence |
| --- | --- | --- |
| Nature des ondes, RF ou acoustique | évaluation du moyen de mesure disponible | tout le reste |
| Fréquence de travail | audit des instruments | dimensions, coût, mesure |
| Nombre d'éléments | budget et complexité | résolution du faisceau |
| Type de déphasage | coût des composants | précision et rôle du FPGA |
| Analogique ou numérique | objectif principal du projet | coût et complexité |
| Méthode de mesure du diagramme | environnement disponible | crédibilité de tous les résultats |
