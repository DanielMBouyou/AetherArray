# 0001. Construire le simulateur avant le réseau

- Statut : acceptée
- Date : 2026-08-21
- Portée : conduite du projet

## Question posée

Faut-il construire d'abord un réseau physique, ou d'abord un simulateur de réseau
avec défauts injectés ?

## Contexte

Sur un réseau réel, on ne connaît pas les défauts réels. On peut donc mesurer si
une calibration améliore le résultat, mais pas si elle a trouvé la bonne réponse.
Or la question du projet porte précisément sur la comparaison de méthodes
d'estimation.

Par ailleurs, le réseau physique dépend d'achats, de fabrication et d'un
environnement de mesure dont la qualité n'est pas encore connue.

## Options étudiées

### Option A : matériel d'abord
Construire le réseau, mesurer, puis développer les méthodes. Avantage : concret,
motivant. Inconvénient : on ne peut pas valider une méthode d'estimation sans
connaître la vérité, et tout dépend de la qualité de l'environnement de mesure.

### Option B : simulateur d'abord
Développer et comparer les méthodes sur un réseau virtuel dont les défauts sont
connus, puis les appliquer au réel. Avantage : la justesse des méthodes est
vérifiable. Inconvénient : rien de physique pendant un moment.

### Option C : en parallèle
Le simulateur avance pendant que le fil matériel progresse, contraint par ses
délais.

## Comparaison

| Critère | A | B | C |
| --- | --- | --- | --- |
| Possibilité de valider la justesse des méthodes | nulle | complète | complète |
| Dépendance aux achats et délais | forte | nulle | partielle |
| Temps avant premier résultat | long | court | court |
| Risque si l'environnement de mesure est mauvais | projet bloqué | aucun impact sur le fil simulation | limité |

## Preuves utilisées

Aucune preuve expérimentale. Argument méthodologique : une méthode d'estimation ne
peut être validée que sur un cas où la vérité est connue, ce qui exclut le réseau
réel.

## Décision

Option C, avec priorité au simulateur. Le simulateur est développé et vérifié en
premier, et le fil matériel démarre par l'audit de l'environnement de mesure, qui
ne coûte rien.

## Conséquences

- Le premier résultat du projet sera une comparaison en simulation.
- Le simulateur doit être vérifié avec soin, puisque tout le fil théorique en
  dépend.
- L'environnement de mesure est caractérisé avant tout achat de composants.

## Limites connues

Un simulateur reproduit ce qu'on a pensé à y mettre. Les défauts qu'on n'a pas
modélisés, par exemple un couplage inattendu ou un effet d'environnement, ne
seront pas capturés. Les conclusions de simulation devront donc être confrontées
au réel, et les écarts analysés plutôt qu'expliqués après coup.

## Conditions de réexamen

- Si l'environnement de mesure se révèle excellent, le fil matériel peut être
  accéléré.
- Si le simulateur devient un projet en soi, réduire son ambition et passer au
  réel.
