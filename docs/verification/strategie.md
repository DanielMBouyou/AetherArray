# Comment on sait qu'un résultat est juste

- Statut : en cours
- Dernière revue : 2026-08-21

## 1. Vérification du simulateur

Le simulateur est le fondement du fil théorique. S'il est faux, tout l'est.

| Contrôle | Valeur attendue |
| --- | --- |
| Diagramme sans défaut, réseau uniforme | largeur de faisceau et niveau de lobes secondaires conformes aux formules classiques |
| Réseau à un seul élément | diagramme de l'élément seul, sans directivité de réseau |
| Pointage demandé à zéro degré | maximum exactement à zéro |
| Pointage demandé à trente degrés | maximum à trente degrés, à la précision de calcul près |
| Espacement supérieur à une demi-longueur d'onde | apparition d'un faisceau parasite, à la position prévue |
| Erreurs de phase nulles | résultat identique au cas idéal |

Ces contrôles sont rapides à écrire et attrapent la quasi-totalité des erreurs
d'implémentation.

## 2. Vérification des méthodes de calibration

| Contrôle | Méthode |
| --- | --- |
| Sans bruit, la méthode retrouve-t-elle exactement les défauts injectés ? | simulation, comparaison directe |
| Avec un défaut nul, la méthode renvoie-t-elle une correction nulle ? | cas témoin |
| La qualité se dégrade-t-elle de façon régulière quand le bruit augmente ? | balayage |
| Le résultat dépend-il de l'ordre des mesures ? | permutation |

Le premier contrôle est le plus important. Une méthode qui ne retrouve pas la
vérité en l'absence de bruit est fausse, et aucune quantité de réglage ne la
sauvera.

## 3. Vérification de la mesure réelle

| Contrôle | Ce qu'il détecte |
| --- | --- |
| Mesure répétée sans rien toucher | bruit de mesure |
| Mesure répétée après remontage | reproductibilité mécanique |
| Mesure avec un seul élément alimenté | comportement de l'élément seul, référence |
| Mesure du diagramme symétrique, réseau retourné | asymétrie du banc ou de l'environnement |
| Vérification de l'effet d'une erreur connue | validation complète de la chaîne |

L'avant-dernier contrôle est astucieux : si l'on retourne physiquement le réseau,
le diagramme mesuré devrait être l'image miroir du précédent. S'il ne l'est pas,
c'est l'environnement qui parle et non le réseau.

Le dernier contrôle correspond à l'expérience EXP-007. Il valide simultanément le
montage, le banc de mesure et la théorie, ce qui en fait l'expérience la plus
rentable du projet.

## 4. Vérification avant publication d'un résultat

- [ ] L'écart observé dépasse-t-il le bruit de mesure répétée ?
- [ ] Les conditions de mesure sont-elles notées, y compris l'environnement ?
- [ ] Le nombre de mesures consommées est-il indiqué ?
- [ ] La comparaison a-t-elle été faite sur plusieurs tirages ou plusieurs
      répétitions ?
- [ ] Les résultats de simulation et de mesure sont-ils clairement distingués ?

## 5. Ce qui n'est pas prévu

- Pas de mesure en chambre anéchoïque, sauf occasion.
- Pas de mesure en champ proche complète, sauf si un positionneur précis devient
  disponible.
- Pas de caractérisation en polarisation croisée dans un premier temps.
