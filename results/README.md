# Résultats

Ce dossier contient les mesures réelles, pas les mesures espérées.

## Organisation

```
results/
  EXP-001-nom/
    SOURCE.md        origine, date, opérateur, matériel, versions
    raw/             données brutes, jamais modifiées
    processed/       données dérivées, régénérables par script
    figures/
    notes.md         ce qui s'est mal passé pendant la manipulation
```

`raw/` est en lecture seule par convention. Si une donnée brute est fausse, on ne
la corrige pas : on ajoute une note et on refait la mesure.

## Règle sur les données brutes

Une mesure sans métadonnée est perdue. `SOURCE.md` doit contenir au minimum :

- date et heure,
- matériel utilisé avec identifiants,
- versions logicielles, de bitstream ou de firmware,
- conditions (température ambiante si pertinent, alimentation, câblage),
- procédure de calibration éventuelle et sa date,
- anomalies constatées.

## Politique de versionnement des gros fichiers

À décider avant la première campagne de mesure sérieuse.

| Option | Avantage | Inconvénient | Statut |
| --- | --- | --- | --- |
| Tout dans git | simple, autonome | dépôt lourd, clone lent | à évaluer |
| Git LFS | intégré à GitHub | quota, friction pour les contributeurs | à évaluer |
| Données hors dépôt, empreintes dans git | dépôt léger | nécessite un stockage externe fiable | à évaluer |
| Sous-échantillon dans git, brut hors dépôt | compromis | risque de désynchronisation | à évaluer |

Tant que la décision n'est pas prise, on limite les fichiers à quelques Mo et on
privilégie les formats texte compressibles.

## Reproductibilité

Chaque figure publiée dans le README ou dans un document doit pouvoir être
régénérée par un script présent dans le dépôt, à partir des données de `raw/`.
Une figure sans script associé est marquée comme illustrative.
