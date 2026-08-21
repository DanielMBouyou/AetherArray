# Stratégie d'intégration continue

- Statut : cible définie
- Dernière revue : 2026-08-21

## État actuel

Seule la vérification de la documentation est active.

## Cible

| Étape | Déclencheur | Ce qui est vérifié | Statut |
| --- | --- | --- | --- |
| 1 | documentation | conventions et structure | actif |
| 2 | simulateur | les cas de référence théoriques sont retrouvés | à venir |
| 3 | méthodes de calibration | en l'absence de bruit, les défauts injectés sont exactement retrouvés | à venir |
| 4 | comparaison | un jeu réduit de tirages redonne les mêmes conclusions | à venir |
| 5 | figures | les figures se régénèrent sans erreur | à venir |

Les étapes 2 et 3 sont les plus utiles. Elles vérifient que le coeur scientifique
du projet fonctionne, en quelques secondes.

## Point d'attention

Les méthodes comparées sont stochastiques : elles dépendent de tirages aléatoires.
En intégration continue, les graines doivent être fixées, sinon les tests échouent
de temps en temps sans raison, ce qui détruit la confiance dans la chaîne.

Les campagnes à graine variable ont leur place, mais lancées volontairement, avec
les graines enregistrées dans les résultats.

## Ce qui restera manuel

- Toutes les mesures physiques.
- Le contrôle de l'environnement de mesure.
- L'interprétation des écarts entre simulation et mesure.
