# Ce que ce projet partage avec les autres

- Statut : observation en cours
- Dernière revue : 2026-08-21

## Lien fort avec NeuralRFIC

Les deux projets utilisent les mêmes instruments, la même méthode de calibration
d'instrument, la même connectique, et probablement le même fabricant de circuits
imprimés.

| Élément partagé | Nature du partage | Recommandation |
| --- | --- | --- |
| Analyseur de réseau vectoriel | ressource physique unique | calendrier d'occupation |
| Procédure de calibration d'instrument | méthode identique | l'écrire une seule fois, la référencer depuis les deux dépôts |
| Automatisation des instruments | même approche, même bibliothèque | duplication assumée au début, extraction plus tard |
| Traitement des paramètres S | même outillage | idem |
| Câbles, atténuateurs, adaptateurs | ressources physiques | inventaire commun utile |
| Commandes de circuits imprimés | frais fixes importants | grouper les commandes |
| Positionneur angulaire | utile aux deux | à concevoir une fois, avec les deux usages en tête |

La dernière ligne est un cas rare de mutualisation matérielle évidente. Un
positionneur commandé par microcontrôleur sert aux mesures de diagramme ici, et aux
mesures répétables là-bas.

## Lien conditionnel avec les projets FPGA

Le FPGA n'intervient dans ce projet que si l'architecture numérique est retenue.
Dans ce cas, deux compétences deviennent directement partagées :

| Élément | Projet source | Usage ici |
| --- | --- | --- |
| Synchronisation précise entre cartes | muMarket | cohérence entre voies de réception |
| Traitement numérique du signal en virgule fixe | FlowTensor | formation de faisceau embarquée |
| Bancs de test RTL | NeuroVerify-SoC | vérification du traitement |

Si l'architecture analogique est retenue, ce lien disparaît, et il faut l'accepter
plutôt que de forcer un usage du FPGA.

## Matériel partagé

| Ressource | Partagée avec | Conflit possible | Gestion |
| --- | --- | --- | --- |
| Analyseur de réseau | NeuralRFIC | oui, fort | calendrier |
| Oscilloscope | tous | oui | calendrier |
| Cartes FPGA | muMarket, FlowTensor, NeuroVerify-SoC | seulement si voie numérique | à arbitrer |
| Microcontrôleurs | tous | faible | usage ponctuel |
| Station de calcul | FlowTensor, NeuralRFIC | faible ici | file d'attente |

## Ce qui ne doit pas être mutualisé

- Les algorithmes de calibration de réseau, spécifiques.
- Le simulateur de réseau d'antennes.
- Les métriques de diagramme.

## Remarque sur le calendrier

Ce projet et NeuralRFIC se disputent le même instrument principal, l'analyseur de
réseau. Les mener strictement en parallèle serait une source de blocages
permanents : une campagne de mesure ne se découpe pas en tranches d'une heure,
puisque démonter un montage calibré fait perdre la calibration. Une alternance par
phases est donc probablement préférable.
