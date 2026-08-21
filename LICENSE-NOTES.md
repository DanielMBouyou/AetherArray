# Choix de licence : analyse, pas encore de décision

- Statut : à trancher avant publication du dépôt
- Dernière revue : 2026-08-21

Aucun fichier `LICENSE` n'est présent volontairement. Poser une licence par
habitude est une décision technique déguisée en formalité.

**Attention** : un dépôt public sans licence n'est pas "libre". En l'absence de
licence, le droit d'auteur s'applique par défaut et personne n'a le droit de
réutiliser le contenu. Ce n'est donc pas un état acceptable à long terme pour un
dépôt destiné à être lu et éventuellement repris.

## 1. Ce que contient le dépôt

Le contenu n'est pas homogène, et une licence unique n'est pas forcément le bon
choix.

| Nature | Présent aujourd'hui | Prévu | Licence adaptée |
| --- | --- | --- | --- |
| Documentation, analyses, figures | oui | oui | famille Creative Commons |
| Code logiciel (scripts, modèle de référence, analyse) | non | oui | licence logicielle permissive ou copyleft |
| Schémas et circuits imprimés | non | probable | licence matérielle dédiée, voir plus bas |
| Fichiers de simulation | non | oui | attention aux modèles de composants fournis par les fabricants |
| Données de mesure produites ici | non | oui | licence de données ou domaine public |
| Données tierces | non | non, par principe | sans objet, on ne les redistribue pas |

## 2. Les candidates

| Licence | Type | Ce qu'elle permet | Ce qu'elle impose | Pertinence ici |
| --- | --- | --- | --- | --- |
| MIT | permissive | tout, y compris usage commercial fermé | attribution | simple, mais aucune clause sur les brevets |
| BSD 2 ou 3 clauses | permissive | idem | attribution | équivalent à MIT en pratique |
| Apache 2.0 | permissive | idem | attribution, mention des modifications, concession de brevets | intéressante pour du matériel, où les brevets existent vraiment |
| MPL 2.0 | copyleft de fichier | usage large | les fichiers modifiés restent ouverts | compromis rarement utilisé en matériel |
| GPL 3.0 | copyleft fort | usage large | toute oeuvre dérivée reste sous GPL | dissuade la reprise industrielle, rarement adapté au RTL |
| CERN OHL, variantes P, W et S | matériel | conçue pour les designs matériels | selon la variante, de permissive à copyleft fort | pensée pour ce cas précis |
| Solderpad | matériel | dérivée d'Apache 2.0 adaptée au matériel | attribution, brevets | utilisée par plusieurs projets RISC-V |
| CC BY 4.0 | documentation | réutilisation avec attribution | attribution | adaptée aux textes et figures |
| CC0 | domaine public | tout | rien | adaptée aux données de mesure |

## 3. Le point qui décidera vraiment

La licence des briques externes reprises. Trois cas :

| Cas | Conséquence |
| --- | --- |
| On n'écrit que du code original | choix totalement libre |
| On reprend des blocs sous licence permissive | choix libre, avec obligation d'attribution et conservation des en-têtes |
| On reprend un bloc sous copyleft fort | la licence du projet est en grande partie déterminée |

Conséquence pratique : **la décision de licence dépend de la décision
d'architecture**, donc elle vient après. Chaque brique externe envisagée doit
avoir sa licence notée dans sa fiche de `research/fiches/`, et c'est cette liste
qui décidera.

## 4. Le cas particulier des dessins de carte

Un dessin de circuit imprimé n'est pas du logiciel. Les licences dédiées au
matériel ouvert ont été écrites précisément pour cet objet, et elles existent en
plusieurs variantes, de la plus permissive à la plus contraignante pour les
travaux dérivés.

Question ouverte : appliquer une licence logicielle par simplicité, ou une licence
matérielle par exactitude ? À trancher, avec un argument.

## 5. Le cas des modèles de composants, des simulations et des données de mesure

Point spécifique à ce projet et facile à oublier : les modèles de composants
fournis par les fabricants sont souvent soumis à des conditions d'utilisation
particulières, et leur redistribution n'est généralement pas autorisée.

Règle du dépôt :

- on ne redistribue aucun modèle de composant fourni par un fabricant,
- on référence le composant et l'endroit où récupérer son modèle,
- les fichiers de simulation présents dans le dépôt doivent pouvoir être ouverts
  sans ces modèles, ou indiquer clairement ce qui manque.

La même prudence s'applique aux données de mesure fournies par des tiers, y
compris les jeux de données publics : leurs conditions d'utilisation doivent être
lues et notées dans la fiche correspondante.

## 6. Proposition de départ, non validée

À discuter, et à confirmer par une fiche de décision :

- documentation et figures : Creative Commons attribution,
- scripts et modèle de référence : Apache 2.0, pour la clause de brevets,
- dessins de carte : à décider, licence matérielle dédiée probable,
- données de mesure produites ici : domaine public ou attribution simple.

Un fichier `LICENSE` par nature de contenu est possible et courant. Cela demande
une explication claire en tête de README pour éviter toute ambiguïté.

## 7. Points de vigilance avant publication

- [ ] Aucune donnée tierce redistribuée sans autorisation.
- [ ] Aucun extrait de documentation constructeur copié dans le dépôt.
- [ ] Aucune clé, aucun jeton, aucune adresse personnelle.
- [ ] Aucun modèle de composant fourni par un fabricant n'est redistribué.
- [ ] Les conditions d'utilisation des jeux de données tiers sont vérifiées.
- [ ] Le fichier de licence choisi est présent avant de rendre le dépôt public.
- [ ] Le README indique clairement quelle licence s'applique à quoi.
