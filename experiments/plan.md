# Plan d'expériences

- Statut : en cours
- Dernière revue : 2026-08-21

Comme dans NeuralRFIC, le travail est organisé en deux fils : un fil simulation qui
démarre immédiatement, et un fil matériel contraint par les achats et la
fabrication.

---

## Vue d'ensemble

| N | Fil | Titre | Débloque | Effort | Statut |
| --- | --- | --- | --- | --- | --- |
| 001 | simulation | Simulateur de réseau avec défauts injectés | tout le fil simulation | 1 semaine | à faire |
| 002 | simulation | Comparaison des méthodes de calibration | résultat principal théorique | 2 semaines | à faire |
| 003 | simulation | Sensibilité au bruit et au nombre de mesures | dimensionnement des campagnes réelles | 1 semaine | à faire |
| 004 | matériel | Audit des instruments et de l'environnement | tout le fil matériel | 2 jours | à faire |
| 005 | matériel | Essai de mesure de puissance reproductible | faisabilité de toute mesure | 2 jours | à faire |
| 006 | matériel | Réseau à deux éléments | premier système réel | 2 semaines | à faire |
| 007 | matériel | Effet d'une erreur de câble connue | démonstration du problème | 1 jour | à faire |
| 008 | matériel | Première calibration réelle | résultat principal pratique | 1 semaine | à faire |
| 009 | matériel | Extension à quatre éléments | résolution et couplage | 2 semaines | à faire |
| 010 | matériel | Durée de validité d'une calibration | axe original | temps calendaire | à faire |

---

## EXP-001 : simulateur de réseau

**Question** : dispose-t-on d'un banc virtuel où les défauts sont connus
exactement ?

**Méthode** : implémenter le facteur de réseau, injecter des erreurs de gain et de
phase tirées au hasard, ajouter du couplage et du bruit de mesure réglables.

**Vérification** : sans défaut ni bruit, le diagramme doit correspondre exactement
à la théorie, largeur de faisceau et niveau de lobes secondaires compris. C'est un
test facile à écrire et qui attrape la plupart des erreurs d'implémentation.

**Livrable** : un simulateur testé, réutilisable pour toutes les expériences
suivantes.

---

## EXP-002 : comparaison en simulation

**Question** : quelle méthode de calibration donne la meilleure qualité pour un
nombre de mesures donné ?

**Méthode** : appliquer chaque méthode au même réseau virtuel, avec les mêmes
défauts et le même bruit, en comptant les mesures consommées. Répéter sur de
nombreux tirages de défauts.

**Livrable** : la courbe qualité en fonction du nombre de mesures, une par méthode.
C'est le résultat central du fil simulation, et il est obtenu sans matériel.

**Critère** : les courbes sont produites, et les croisements éventuels sont
expliqués.

---

## EXP-005 : mesure de puissance reproductible

**Question** : peut-on mesurer une puissance reçue de façon reproductible dans
l'environnement disponible ?

**Méthode** : montage fixe, mesure répétée sur plusieurs minutes, puis après avoir
déplacé un objet dans la pièce, puis avec quelqu'un qui passe à proximité.

**Critère** : écart type des mesures répétées. Ce chiffre devient le plancher
d'incertitude et détermine si les mesures de diagramme sont possibles.

**Pourquoi c'est prioritaire** : si la variation due à l'environnement dépasse
l'effet qu'on veut mesurer, il faut changer de stratégie immédiatement, avant tout
achat.

---

## EXP-007 : démonstration du problème

**Question** : quel est l'effet mesurable d'une erreur de longueur de câble connue ?

**Méthode** : réseau à deux éléments, mesure du diagramme, puis remplacement d'un
câble par un câble un peu plus long, de longueur connue, et nouvelle mesure.

**Hypothèse à écrire avant** : le déphasage introduit vaut environ 4,4 degrés par
millimètre à 2,4 GHz dans un câble à vitesse de propagation usuelle. La direction
du faisceau doit se déplacer d'une quantité calculable à partir de cette valeur.

**Critère** : accord entre le déplacement prévu et le déplacement mesuré.

**Pourquoi cette expérience est importante** : c'est la démonstration la plus
parlante du projet, et elle valide en même temps le banc de mesure. Si le
déplacement mesuré correspond au calcul, on sait que tout le montage fonctionne et
qu'on mesure bien ce qu'on croit mesurer.

---

## Suite

Les expériences 008 à 010 seront détaillées quand les précédentes auront eu lieu.
EXP-010, sur la durée de validité, demande peu de travail mais du temps calendaire.
Elle peut donc être lancée en parallèle des autres.
