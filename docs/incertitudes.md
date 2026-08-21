# Ce qui est certain, supposé, ou à vérifier

- Statut : en cours
- Dernière revue : 2026-08-21

---

## 1. Certain

| Fait | Source | Conséquence |
| --- | --- | --- |
| Un centimètre de câble coaxial vaut environ 44 degrés de phase à 2,4 GHz | calcul à partir de la vitesse de propagation | la calibration est obligatoire, pas optionnelle |
| Des erreurs de phase d'écart type 30 degrés coûtent environ 1,2 dB de gain | résultat classique sur les réseaux | l'effet est chiffrable avant toute mesure |
| Un espacement supérieur à une demi-longueur d'onde crée des faisceaux parasites | condition de non-repliement | contrainte géométrique stricte |
| La distance de champ lointain vaut environ deux fois le carré de la taille du réseau divisé par la longueur d'onde | définition usuelle | fixe la distance de mesure |
| Un corps humain proche du montage modifie la mesure | absorption et réflexion | protocole de mesure à respecter |
| Le déphasage nécessaire dépend de la fréquence | forme du facteur de réseau | le pointage dérive avec la fréquence |

## 2. Supposé

| Hypothèse | Pourquoi on la fait | Comment elle peut tomber | Effet si elle tombe |
| --- | --- | --- | --- |
| Les mesures de diagramme sont possibles dans une pièce ordinaire | avec précautions, beaucoup y arrivent | si les réflexions dominent | passer à la mesure au contact, ou à un réseau acoustique |
| Le couplage entre éléments est secondaire devant les erreurs de voie | espacement d'une demi-longueur d'onde | si le couplage est fort | il faut estimer la matrice complète, donc plus de mesures |
| Une méthode classique de calibration suffira | maturité du domaine | si elle échoue face au bruit ou au couplage | l'optimisation devient nécessaire, ce qui est intéressant |
| Deux éléments suffisent pour valider la méthode | la physique est la même | si les phénomènes intéressants n'apparaissent qu'à partir de quatre | passer à quatre plus tôt |
| Un réseau acoustique est un bon substitut pour les algorithmes | même formalisme mathématique | si les différences physiques changent les conclusions | valider sur les deux, ce qui est justement l'expérience intéressante |

## 3. À vérifier

| N | Question | Méthode | Bloquant pour |
| --- | --- | --- | --- |
| I1 | Peut-on mesurer une puissance reçue de façon reproductible ? | EXP-005 | tout le fil matériel |
| I2 | L'analyseur de réseau permet-il un fenêtrage temporel pour isoler le trajet direct ? | documentation et essai | qualité des mesures |
| I3 | Quelle est l'amplitude réelle des réflexions dans l'environnement disponible ? | EXP-005 | choix de la stratégie de mesure |
| I4 | Peut-on mesurer la phase, ou seulement la puissance ? | audit des instruments | choix de la méthode de calibration |
| I5 | Quel est le niveau réel des erreurs de voie dans un montage fait maison ? | EXP-006 | dimensionnement de la calibration |
| I6 | Le couplage entre éléments est-il significatif à l'espacement retenu ? | mesure des paramètres S entre éléments | complexité du modèle |
| I7 | Quel est le coût des déphaseurs commandables ? | recherche de composants | choix de l'architecture |
| I8 | Combien de temps une calibration reste-t-elle valable ? | EXP-010 | usage pratique du système |
| I9 | Un positionneur angulaire est-il nécessaire, et peut-on le fabriquer ? | essai | faisabilité des mesures de diagramme |
| I10 | Le FPGA est-il réellement utile ici ? | choix d'architecture | rôle du projet dans le laboratoire |

La question I10 mérite d'être posée franchement. Si l'architecture retenue est
analogique, le FPGA ne sert à rien dans ce projet, et il faut l'assumer plutôt que
de lui trouver un rôle artificiel.

## 4. Erreurs de raisonnement à éviter

- **Mesurer un diagramme sans caractériser l'environnement.** Les échos peuvent
  produire des courbes qui ressemblent à des lobes.
- **Attribuer au couplage ce qui vient des câbles.** Les deux se confondent dans la
  mesure, il faut un protocole pour les séparer.
- **Comparer des méthodes de calibration sans compter les mesures.**
- **Conclure sur un seul tirage de défauts.** Les résultats varient beaucoup d'un
  tirage à l'autre.
- **Oublier que l'opérateur fait partie du montage.**
- **Croire qu'une calibration est définitive.** C'est justement ce qu'il faut
  mesurer.
- **Utiliser un FPGA parce qu'il est disponible**, alors que l'architecture retenue
  n'en a pas besoin.
