# Journal des décisions

Ce dossier conserve les décisions techniques structurantes du projet.

## Pourquoi

Dans six mois, la question ne sera pas "qu'est-ce qu'on a choisi", elle sera
"pourquoi on a choisi ça, et est-ce que la raison tient toujours". Un choix sans
justification tracée finit par être repris par habitude, même quand le contexte a
changé.

## Ce qui mérite une entrée

Une décision entre ici si au moins une de ces conditions est vraie :

- elle est coûteuse à annuler (matériel acheté, architecture RTL engagée, format
  de données figé),
- elle exclut une famille de solutions,
- elle repose sur une hypothèse qui pourrait se révéler fausse,
- quelqu'un d'extérieur pourrait raisonnablement faire l'autre choix.

Un choix réversible en une heure ne mérite pas de fiche.

## Format

Un fichier par décision : `NNNN-titre-court.md`, à partir de `0001`. La
numérotation ne recule jamais. Une décision annulée n'est pas supprimée : son
statut passe à `remplacée par NNNN` et la nouvelle fiche explique ce qui a changé.

Statuts possibles : `proposée`, `acceptée`, `rejetée`, `remplacée`, `suspendue`.

Le modèle est dans `0000-template.md`.

## Règle importante pour cette phase

Le projet est en phase d'étude. La plupart des grandes questions ne doivent pas
encore être tranchées. Une fiche de décision écrite trop tôt, sans mesure, est une
manière déguisée de figer une intuition. Si une décision doit être prise sans
preuve (contrainte de calendrier ou de budget), la fiche doit le dire dans la
section "preuves" plutôt que d'inventer une justification technique.
