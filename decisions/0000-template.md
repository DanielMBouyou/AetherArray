# NNNN. Titre court de la décision

- Statut : proposée | acceptée | rejetée | remplacée par NNNN | suspendue
- Date : AAAA-MM-JJ
- Portée : quel sous-système est concerné

## Question posée

Formuler la question sous une forme qui admet plusieurs réponses défendables.
Si la question n'a qu'une réponse possible, ce n'est pas une décision, c'est une
contrainte : la documenter ailleurs.

## Contexte

Ce qui est vrai au moment de la décision : contraintes matérielles, temps
disponible, compétences, dépendances avec d'autres choix déjà faits.

## Options étudiées

### Option A
Description, ce qu'elle apporte, ce qu'elle coûte.

### Option B
Idem.

### Option C, ou "ne rien décider pour l'instant"
L'option "attendre d'avoir mesuré" est légitime. La lister quand elle est
raisonnable.

## Comparaison

| Critère | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Performance attendue | à mesurer | à mesurer | à mesurer |
| Complexité de mise en oeuvre | | | |
| Coût matériel | | | |
| Reproductibilité par un tiers | | | |
| Risque principal | | | |
| Réversibilité | | | |

## Preuves utilisées

Lister précisément. Pour chaque preuve, dire sa nature :

- mesure faite ici : lien vers `results/EXP-NNN`
- résultat de simulation : préciser l'outil et sa version
- source externe : référence complète
- avis technique non vérifié : le dire

Si cette section est vide, l'écrire noir sur blanc : "aucune preuve
expérimentale, décision prise sur la base de X".

## Décision

Ce qui est décidé, en une ou deux phrases, sans ambiguïté.

## Conséquences

- Ce que cela rend possible.
- Ce que cela rend plus difficile ou impossible.
- Travail induit (code à écrire, matériel à acheter, compétence à acquérir).

## Limites connues

Ce que la décision ne résout pas, et les cas où elle est probablement mauvaise.

## Conditions de réexamen

Formuler des déclencheurs observables, pas une date vague. Par exemple :
"si la latence mesurée dépasse X", "si le taux d'occupation DSP dépasse Y",
"si le composant Z devient indisponible".
