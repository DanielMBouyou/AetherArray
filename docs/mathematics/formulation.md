# Formulation mathématique

- Statut : en cours
- Dernière revue : 2026-08-21

---

## 1. Le facteur de réseau

Pour un réseau linéaire de `N` éléments identiques, régulièrement espacés de `d` :

```
AF(θ) = somme sur n de 0 à N-1 de :  a_n · exp( j ( n·k·d·sin θ + φ_n ) )
```

- `a_n` : amplitude appliquée à l'élément `n`, sans unité.
- `φ_n` : phase appliquée à l'élément `n`, en radians. C'est la commande.
- `k = 2π/λ` : nombre d'onde, en radians par mètre. Il traduit une distance en
  déphasage.
- `d·sin θ` : différence de trajet entre deux éléments voisins, vue depuis la
  direction `θ`.
- `n·k·d·sin θ` : déphasage accumulé pour l'élément `n`.

Pourquoi la fonction exponentielle complexe : elle représente une onde par un
vecteur tournant. Additionner des ondes revient alors à additionner des vecteurs.
Quand ils pointent dans la même direction, les amplitudes s'ajoutent. Quand ils
sont opposés, ils s'annulent. Tout le comportement du réseau tient dans cette
image.

Le champ total rayonné vaut, en toute rigueur, le produit du facteur de réseau par
le diagramme d'un élément seul :

```
diagramme total(θ) = diagramme d'un élément(θ) × AF(θ)
```

Cette factorisation suppose que tous les éléments rayonnent de la même façon, ce
qui est faux en présence de couplage. C'est la première approximation à
questionner.

## 2. Le pointage

Pour pointer dans la direction `θ0`, on choisit :

```
φ_n = - n · k · d · sin θ0
```

Interprétation : on retarde volontairement chaque élément juste ce qu'il faut pour
que toutes les contributions arrivent en phase dans la direction voulue.

Deux conséquences importantes.

**Le repliement de réseau.** Si `d > λ/2`, il existe d'autres directions où les
contributions s'additionnent également, et le réseau émet des faisceaux parasites
aussi forts que le principal. C'est pour cette raison que l'espacement usuel est
`λ/2`. On peut le dépasser, à condition de savoir ce qu'on accepte.

**La déviation en fréquence.** La phase requise dépend de `k`, donc de la
fréquence. Un réseau réglé pour pointer à 30 degrés à une fréquence donnée pointera
légèrement ailleurs à une autre fréquence. Sur une bande étroite l'effet est
faible, sur une large bande il devient gênant. La vraie solution consiste à
appliquer un retard temporel plutôt qu'un déphasage, ce qui est plus coûteux.

## 3. Quelques grandeurs utiles

| Grandeur | Expression approximative | Interprétation |
| --- | --- | --- |
| Largeur du faisceau à mi-puissance | environ `0,886 λ / (N·d)` radians, au pointage zéro | plus le réseau est grand devant la longueur d'onde, plus le faisceau est fin |
| Niveau du premier lobe secondaire, amplitudes uniformes | environ -13,2 dB | valeur fixe, indépendante de `N` |
| Gain de réseau | environ `10·log10(N)` dB par rapport à un élément | doubler le nombre d'éléments ajoute 3 dB |
| Élargissement au dépointage | facteur `1/cos θ0` | le faisceau s'élargit quand on s'éloigne de l'axe |

Le dernier point est souvent négligé : un réseau qui pointe à 60 degrés a un
faisceau environ deux fois plus large qu'au centre, parce que sa surface apparente
vue depuis cette direction est réduite.

## 4. L'effet des erreurs

Si les phases réelles s'écartent des phases voulues d'une quantité aléatoire
d'écart type `σ` en radians, le gain moyen se dégrade approximativement selon :

```
G_réel / G_idéal ≈ exp( - σ² )
```

| Écart type de phase | Perte de gain | Effet sur les lobes secondaires |
| --- | --- | --- |
| 5 degrés | négligeable | négligeable |
| 15 degrés | environ 0,3 dB | léger |
| 30 degrés | environ 1,2 dB | notable |
| 45 degrés | environ 2,7 dB | important, diagramme dégradé |

Ce tableau explique pourquoi la calibration n'est pas un raffinement mais une
nécessité. Il montre aussi que la perte de gain n'est pas le pire : l'énergie
perdue dans le faisceau principal se retrouve dans les lobes secondaires, ce qui
est souvent plus gênant en pratique.

## 5. Le modèle matriciel

On rassemble tous les défauts dans une matrice :

```
y = H · x
```

- `x` : vecteur des commandes, `N` valeurs complexes.
- `y` : vecteur des signaux réellement présents aux éléments.
- `H` : matrice `N × N` complexe.

Structure de `H` :

- les termes diagonaux `H_nn` décrivent le gain et la phase propres à chaque voie,
- les termes hors diagonale `H_nm` décrivent le couplage entre les éléments `n` et
  `m`.

Si le couplage est négligeable, `H` est diagonale et la calibration se réduit à
`N` corrections indépendantes. C'est le cas simple, et il faut vérifier s'il
s'applique plutôt que le supposer.

## 6. Le problème inverse

### Cas surdéterminé

Avec `M` mesures et `N` inconnues, si `M > N`, la solution aux moindres carrés
s'écrit :

```
x_estimé = (A^H A)^(-1) A^H b
```

où `A` est la matrice décrivant les conditions de mesure, `b` le vecteur des
mesures et `A^H` la transposée conjuguée.

### Conditionnement et régularisation

Si `A` est mal conditionnée, c'est à dire si certaines combinaisons d'inconnues
sont mal contraintes par les mesures, une petite erreur de mesure produit une
grande erreur d'estimation. Le nombre de conditionnement mesure ce risque.

La régularisation consiste à ajouter une contrainte :

```
x_estimé = (A^H A + λ I)^(-1) A^H b
```

Le terme `λ I` stabilise l'inversion au prix d'un léger biais. Interprétation : on
préfère une solution un peu fausse mais robuste à une solution exacte en théorie et
absurde en pratique. Le choix de `λ` est lui-même une question, traitée par
validation croisée.

### Le cas des mesures de puissance seules

Beaucoup de montages simples ne mesurent qu'une puissance, donc `|y|²`, et perdent
la phase. Retrouver `x` à partir de modules seuls est un problème connu et
difficile, appelé récupération de phase.

Une méthode classique du domaine des réseaux d'antennes contourne élégamment le
problème : on fait varier la phase d'une seule voie et on observe la puissance
totale. Cette puissance varie de façon sinusoïdale, et la position de son maximum
donne la phase relative de cette voie par rapport à la somme des autres. En
répétant pour chaque voie, on reconstruit toutes les phases relatives sans jamais
mesurer une phase directement.

C'est un bel exemple de méthode qui remplace un instrument coûteux par un
raisonnement. Elle mérite d'être étudiée en priorité, y compris sa sensibilité au
bruit et le nombre de mesures qu'elle demande.

## 7. Formuler la calibration comme une optimisation

Alternative au problème inverse : chercher directement la commande qui maximise un
critère, sans estimer `H`.

```
x* = argmax  f(x)
```

où `f` peut être la puissance mesurée dans une direction, ou l'opposé de l'écart à
un diagramme cible.

| Méthode | Nombre d'évaluations attendu | Robustesse au bruit | Remarque |
| --- | --- | --- | --- |
| Descente de gradient | dépend, gradient difficile à obtenir par la mesure | faible | peu adapté à des mesures bruitées |
| Recuit simulé | élevé | bonne | simple à mettre en oeuvre |
| Stratégie d'évolution | élevé | bonne | robuste mais gourmand en mesures |
| Optimisation bayésienne | faible | bonne | conçue pour les évaluations coûteuses |

La dernière ligne est celle où l'apprentissage a une justification claire :
l'optimisation bayésienne construit un modèle probabiliste de la fonction à
optimiser et choisit chaque mesure pour être la plus informative possible. Quand
une mesure prend plusieurs minutes, réduire leur nombre d'un facteur trois est un
gain réel et directement mesurable.

C'est l'angle le plus défendable pour introduire des méthodes d'apprentissage dans
ce projet, bien plus que d'entraîner un réseau de neurones à prédire un diagramme.

## 8. Distinguer deux problèmes voisins

Ils sont souvent confondus et n'ont pas la même solution.

| Problème | Ce qu'on cherche | Ce qu'il faut mesurer |
| --- | --- | --- |
| Calibration | la matrice `H`, donc l'état du système | des mesures informatives sur chaque voie |
| Synthèse de diagramme | la commande `x` donnant un diagramme cible | le diagramme obtenu |

Une calibration réussie permet ensuite de synthétiser n'importe quel diagramme
sans nouvelle mesure. Une optimisation directe donne un bon résultat pour une
cible, et tout est à refaire pour la suivante.

C'est un compromis intéressant : la calibration coûte cher une fois, l'optimisation
directe coûte à chaque fois. Le point d'équilibre dépend du nombre de diagrammes
différents qu'on veut produire, et ce raisonnement sera fait explicitement.

## 9. Ce qui reste à écrire

- La modélisation du couplage à partir des paramètres S mesurés, et son lien exact
  avec la matrice `H`.
- La notion de diagramme d'élément incorporé, qui remplace l'hypothèse d'éléments
  identiques.
- Le modèle d'impédance active, qui décrit le fait que l'impédance vue par un
  élément dépend de ce que font les autres.
- Le modèle de bruit de mesure, indispensable pour comparer les méthodes
  honnêtement.
