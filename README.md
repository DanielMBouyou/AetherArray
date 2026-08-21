# AetherArray

Un petit réseau d'antennes commandé électroniquement, et surtout l'étude de ce
qui se passe quand on essaie de le faire fonctionner comme la théorie le prévoit.

- Statut : recherche d'architecture et étude de faisabilité
- Dernière revue : 2026-08-21

> Rien n'est encore construit : ni réseau, ni banc de mesure, ni calibration. Ce
> dépôt est un carnet de laboratoire public. La fréquence de travail, et même la
> nature des ondes utilisées, restent ouvertes : ces choix dépendent de ce que
> l'environnement de mesure permet réellement, ce qui n'a pas encore été audité.

---

## L'idée en une image

Un réseau d'antennes est un ensemble de petites antennes alimentées séparément.
En jouant sur la phase du signal envoyé à chacune, on fait tourner le faisceau
sans rien déplacer mécaniquement.

```
   élément 0      élément 1      élément 2      élément 3
      |               |              |              |
    phase φ0       phase φ1       phase φ2       phase φ3
      |               |              |              |
      +---------------+--------------+--------------+
                          |
                   même signal source
```

Si tous les éléments émettent en phase, le faisceau part tout droit. Si on décale
progressivement les phases, il s'incline. C'est le principe des radars modernes et
des antennes de stations de base.

En théorie, c'est simple. En pratique, un réseau réel ne pointe jamais exactement
où on lui demande, et c'est de là que vient tout l'intérêt du projet.

---

## Le modèle idéal, et pourquoi il est faux

Le comportement théorique d'un réseau linéaire s'écrit :

```
AF(θ) = somme sur n de 0 à N-1 de :  a_n · exp( j ( n·k·d·sin θ + φ_n ) )
```

Décomposons chaque terme.

- `N` est le nombre d'éléments.
- `a_n` est l'amplitude envoyée à l'élément `n`.
- `φ_n` est la phase qu'on lui applique. C'est notre levier de commande.
- `d` est l'espacement entre deux éléments voisins, en mètres.
- `k = 2π/λ` est le nombre d'onde. Il convertit une distance en un déphasage :
  parcourir une longueur d'onde fait tourner la phase de 360 degrés.
- `θ` est l'angle d'observation, mesuré par rapport à la perpendiculaire au réseau.
- Le terme `n·k·d·sin θ` est le déphasage naturel dû au fait que l'onde issue de
  l'élément `n` parcourt une distance différente pour atteindre l'observateur.
- `AF(θ)` est le champ résultant dans la direction `θ`, obtenu en additionnant les
  contributions de tous les éléments.

Ce que dit cette formule : les contributions s'additionnent quand elles arrivent
en phase, et s'annulent quand elles arrivent en opposition. Pour pointer le
faisceau dans une direction `θ0`, il suffit de choisir :

```
φ_n = - n · k · d · sin θ0
```

Autrement dit, on compense à l'avance le déphasage naturel dû à la géométrie.

Quelques ordres de grandeur, pour un réseau de 4 éléments espacés d'une
demi-longueur d'onde :

| Grandeur | Valeur approximative | Signification |
| --- | --- | --- |
| Largeur du faisceau | environ 25 degrés | le faisceau n'est pas fin, avec seulement 4 éléments |
| Niveau des lobes secondaires | environ -13 dB | il reste de l'énergie ailleurs que dans le faisceau |
| Gain de réseau | environ 6 dB par rapport à un élément seul | doubler le nombre d'éléments ajoute 3 dB |

Ces chiffres viennent de la théorie et supposent que tout est parfait.

---

## Pourquoi rien n'est parfait

Voici le calcul qui justifie à lui seul l'existence du projet.

Dans un câble coaxial ordinaire, l'onde se propage à environ 66 pour cent de la
vitesse de la lumière. À 2,4 GHz, la longueur d'onde dans le câble vaut donc :

```
λ_câble = 0,66 × 3.10^8 / 2,4.10^9 ≈ 82 mm
```

Un millimètre de câble correspond donc à un déphasage de :

```
360° / 82 mm ≈ 4,4 degrés par millimètre
```

**Un centimètre de différence de longueur entre deux câbles introduit environ 44
degrés d'erreur de phase.** Autant dire que couper les câbles à la main détruit le
diagramme.

Et ce n'est qu'une source d'erreur parmi d'autres :

| Source d'erreur | Origine | Ordre de grandeur | Corrigeable ? |
| --- | --- | --- | --- |
| Longueur de câble | fabrication | des dizaines de degrés | oui, par calibration |
| Tolérance des composants | dispersion de fabrication | quelques degrés à quelques dB | oui |
| Couplage entre éléments voisins | les antennes se voient entre elles | dépend de l'espacement, souvent notable | partiellement |
| Dérive thermique | variation de température | quelques degrés | oui, si on recalibre |
| Connecteurs | serrage, usure | quelques degrés | oui, mais variable |
| Environnement | réflexions sur les objets alentour | très variable | non, il faut maîtriser le lieu de mesure |

L'effet cumulé est net. Une règle utile : si les erreurs de phase ont un écart type
`σ` exprimé en radians, la perte de gain vaut approximativement :

```
perte de gain ≈ exp( - σ² )
```

Pour `σ = 30 degrés`, soit environ 0,52 radian, cela donne une perte d'environ
1,2 dB, et surtout une remontée des lobes secondaires, qui est souvent plus gênante
que la perte de gain elle-même.

Traduction : un réseau non calibré fonctionne, mais mal, et de façon imprévisible.

---

## Le modèle réaliste

Plutôt que de traiter chaque défaut séparément, on les rassemble dans une seule
matrice complexe :

```
y = H · x
```

- `x` est le vecteur des commandes qu'on applique, une valeur complexe par voie
  (amplitude et phase demandées).
- `y` est le vecteur de ce qui sort réellement de chaque élément.
- `H` est une matrice complexe qui contient tout : les erreurs de gain et de
  phase de chaque voie sur sa diagonale, et le couplage entre éléments hors
  diagonale.

Si `H` était l'identité, le système serait parfait. Elle ne l'est pas.

Calibrer, c'est mesurer `H`, puis appliquer une commande corrigée :

```
x_corrigé = H^-1 · x_souhaité
```

C'est là que le projet devient un problème de mathématiques appliquées plutôt que
de bricolage : mesurer `H` demande des mesures, chaque mesure coûte du temps, et
l'inversion peut être instable si la matrice est mal conditionnée.

---

## Les vraies questions du projet

1. **Combien de mesures faut-il pour calibrer ?** Un réseau à `N` voies a au moins
   `N` inconnues complexes, souvent bien plus si l'on veut le couplage. Chaque
   mesure prend du temps et introduit du bruit.
2. **Peut-on calibrer sans mesurer la phase ?** Beaucoup de montages simples ne
   mesurent qu'une puissance. Retrouver des phases à partir de puissances seules
   est un problème mathématique classique et non trivial.
3. **Une méthode classique suffit-elle ?** Moindres carrés, régularisation,
   inversion directe : ces méthodes sont anciennes, éprouvées et peu coûteuses. Il
   faut savoir jusqu'où elles vont avant de parler d'autre chose.
4. **Une méthode d'optimisation peut-elle réduire le nombre de mesures ?** C'est là
   que l'apprentissage a une chance d'apporter quelque chose de réel, et de
   mesurable.
5. **Combien de temps une calibration reste-t-elle valable ?** Question rarement
   traitée, facile à mesurer, et directement utile.

L'ordre est volontaire. Le projet ne commence pas par l'apprentissage automatique,
il commence par ce qui marche déjà, et cherche ensuite où cela ne suffit plus.

---

## La difficulté qu'il ne faut pas sous-estimer : mesurer

Pour caractériser un diagramme de rayonnement, il faut se placer suffisamment loin
pour que l'onde soit devenue plane. La distance minimale usuelle vaut :

```
R > 2 D² / λ
```

où `D` est la plus grande dimension du réseau et `λ` la longueur d'onde.

Exemple numérique, réseau de 4 éléments à 2,4 GHz, espacement de 6,25 cm, donc
`D ≈ 19 cm` et `λ = 12,5 cm` :

```
R > 2 × 0,19² / 0,125 ≈ 0,58 m
```

Moins d'un mètre : c'est faisable sur une table. Mais dans une pièce ordinaire, le
signal se réfléchit sur les murs, le sol, les meubles et l'opérateur. Ces échos
s'additionnent au signal direct et peuvent créer des variations de plusieurs
décibels, c'est à dire du même ordre que ce qu'on cherche à mesurer.

C'est le vrai obstacle du projet. Trois voies possibles, aucune choisie :

| Voie | Principe | Avantage | Inconvénient |
| --- | --- | --- | --- |
| Mesure en espace libre soignée | absorbants, distance, mesures différentielles | réaliste | qualité incertaine, coût des absorbants |
| Mesure au contact, voie par voie | on mesure chaque voie séparément avec un câble | très reproductible | ne mesure pas le couplage rayonné |
| Mesure en champ proche | sonde déplacée près du réseau, puis calcul | précis | demande un déplacement mécanique précis |
| Descente en fréquence | travailler à plus basse fréquence | tout devient plus facile à mesurer | réseau physiquement plus grand |

Il existe une cinquième voie, moins évidente, qui mérite d'être étudiée
sérieusement : **valider les algorithmes de calibration sur un réseau acoustique**.
À 40 kHz dans l'air, la longueur d'onde vaut environ 8,6 mm, les transducteurs
coûtent quelques euros, la mesure se fait avec un microphone, et toute la théorie
du réseau d'antennes s'applique à l'identique. Le problème mathématique est
strictement le même, le matériel est trivial, et l'environnement de mesure est
beaucoup plus facile à maîtriser.

Cette voie n'est pas un repli. Elle permettrait de développer et de valider toute
la partie algorithmique dans de bonnes conditions, puis de l'appliquer au réseau
RF en sachant qu'elle fonctionne. Elle sépare deux risques au lieu de les
additionner.

---

## Ce que le projet va comparer

| Configuration | Ce qu'elle représente |
| --- | --- |
| Simulation idéale | ce que la théorie prévoit |
| Système réel non calibré | ce qu'on obtient sans rien faire |
| Calibration classique | inversion, moindres carrés, régularisation |
| Calibration optimisée | recherche du meilleur réglage par optimisation |
| Méthode assistée par apprentissage | si elle apporte quelque chose |

Avec, pour chacune : erreur de pointage, gain obtenu, niveau des lobes
secondaires, largeur du faisceau, nombre de mesures nécessaires, temps de
calibration, et stabilité dans le temps.

---

## Ce qui est encore ouvert

1. La fréquence de travail, et même la nature des ondes utilisées.
2. Le nombre d'éléments. Quatre est probablement le bon compromis pour commencer.
3. La méthode de déphasage : composants dédiés, commutation, ou génération
   numérique.
4. Le rôle exact du FPGA, qui n'est pas acquis. Un microcontrôleur suffit peut-être
   pour piloter des déphaseurs.
5. Le moyen de mesure du diagramme.
6. La méthode de calibration.

Le point 4 mérite d'être souligné. Le FPGA n'est justifié que si l'on fait de la
formation de faisceau numérique, c'est à dire si l'on traite plusieurs voies
échantillonnées simultanément. Si le déphasage est fait par des composants
analogiques, un microcontrôleur suffit largement. Ce choix doit être fait sur des
arguments, pas parce qu'un FPGA est disponible.

## Ce qui existe déjà, en bref

| Origine | Ce qu'on y trouve | Ce qu'on n'y trouve pas |
| --- | --- | --- |
| Académique | théorie des réseaux, couplage mutuel, méthodes de calibration dont certaines n'utilisent que des mesures de puissance, problèmes inverses | le nombre de mesures physiques réellement nécessaires, comparé entre méthodes |
| Industrie | kits pédagogiques entièrement documentés, circuits de formation de faisceau, notes d'application | la durée de validité d'une calibration hors enceinte climatique |
| Open source | traitement de paramètres S, optimisation bayésienne, projets amateurs qui documentent leurs échecs | une validation croisée entre un réseau radiofréquence et un réseau acoustique |

Le détail est dans `research/etat-de-l-art.md`. Deux méthodes de calibration
méritent d'être lues avant tout le reste : celle qui n'exige que des mesures de
puissance, et celle qui utilise le couplage entre éléments comme moyen de mesure
interne. La seconde, si elle fonctionne à notre échelle, supprimerait le besoin
d'un banc de mesure de diagramme, ce qui changerait complètement le projet.

## Comment le projet sera évalué

La ressource comptée n'est pas le temps de calcul, c'est le **nombre de mesures
physiques**. Une mesure demande un déplacement mécanique, une stabilisation et une
acquisition bruitée. Le calcul associé, lui, prend quelques millisecondes.

| Critère | Seuil |
| --- | --- |
| Nombre de mesures consommées par la méthode | obligatoire à côté de tout résultat de calibration |
| Validation en simulation, où les défauts injectés sont connus | obligatoire, c'est le seul cas où la justesse est vérifiable |
| Reproductibilité de la mesure chiffrée | obligatoire, elle fixe le seuil de signification |
| Répétition sur plusieurs tirages de défauts | obligatoire, un seul tirage ne conclut pas |
| Conditions de mesure et environnement notés | obligatoire, les échos de la pièce se confondent avec des lobes |
| Étiquetage simulé contre mesuré | obligatoire |

Le témoin de référence est le réseau non calibré. C'est lui qui donne la mesure de
ce que la calibration apporte vraiment.

## Comment lire ce dépôt

| Vous voulez | Allez voir |
| --- | --- |
| le périmètre et les questions | `docs/cadrage.md` |
| les équations expliquées | `docs/mathematics/formulation.md` |
| les architectures candidates | `docs/architecture/options.md` |
| le problème de la mesure | `docs/hardware/inventaire-et-besoins.md` |
| les méthodes de calibration comparées | `benchmarks/methodologie.md` |
| ce qui existe déjà | `research/etat-de-l-art.md` |

## Licence

Non définie à ce stade. Le dépôt contiendra du code, des mesures et probablement
des dessins de circuit imprimé. Analyse dans `LICENSE-NOTES.md`.
