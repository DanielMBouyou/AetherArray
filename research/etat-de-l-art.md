# État de l'art : réseaux à commande de phase et calibration

- Statut : brouillon structuré, lectures à faire
- Dernière revue : 2026-08-21

Références notées de mémoire, à vérifier à la première lecture.

---

## 1. Académique

### 1.1 Fondamentaux des réseaux d'antennes

| Réf | Piste | Priorité | Question visée | État |
| --- | --- | --- | --- | --- |
| A1 | Ouvrage de référence sur la théorie des antennes | 1 | facteur de réseau, diagrammes, gain, vocabulaire | à trouver |
| A2 | Ouvrage de référence sur les réseaux à commande de phase | 1 | architectures réelles, contraintes pratiques | à trouver |
| A3 | Travaux sur le couplage mutuel et le diagramme d'élément incorporé | 1 | ce qui invalide le modèle idéal | à trouver |
| A4 | Travaux sur l'impédance active | 2 | pourquoi l'adaptation change quand on dépointe | à trouver |
| A5 | Pondérations d'amplitude pour réduire les lobes secondaires | 2 | compromis largeur de faisceau contre lobes secondaires | à trouver |

### 1.2 Calibration

| Réf | Piste | Priorité | Question visée | État |
| --- | --- | --- | --- | --- |
| A6 | Méthode de calibration par rotation de phase, n'utilisant que des mesures de puissance | 1 | méthode centrale du projet, peu coûteuse en matériel | à trouver |
| A7 | Calibration exploitant le couplage entre éléments voisins | 1 | calibration sans mesure externe, très élégant | à trouver |
| A8 | Calibration en champ proche | 2 | précision, mais matériel de déplacement nécessaire | à trouver |
| A9 | Travaux sur les erreurs de réalisation et leur effet statistique sur le diagramme | 1 | justifie quantitativement la calibration | à trouver |
| A10 | Effet de la quantification de phase | 2 | pertinent si des déphaseurs à pas discrets sont utilisés | à trouver |

A7 mérite une attention particulière : certaines méthodes utilisent le couplage
entre éléments voisins, habituellement considéré comme un défaut, comme moyen de
mesure interne. Le réseau se calibre alors lui-même, sans instrument externe. Si
cette approche fonctionne à notre échelle, elle change complètement le projet en
supprimant le besoin d'un banc de mesure de diagramme.

### 1.3 Problèmes inverses et optimisation

| Réf | Piste | Priorité | Question visée | État |
| --- | --- | --- | --- | --- |
| A11 | Régularisation des problèmes inverses mal posés | 1 | stabilité de l'inversion | à trouver |
| A12 | Récupération de phase à partir de mesures d'intensité | 2 | cas des mesures de puissance seules | à trouver |
| A13 | Optimisation bayésienne et processus gaussiens | 1 | réduire le nombre de mesures physiques | à trouver |
| A14 | Stratégies d'évolution pour l'optimisation sans gradient | 2 | méthode robuste de référence | à trouver |
| A15 | Synthèse de diagramme par optimisation | 2 | obtenir un diagramme cible | à trouver |

### 1.4 Apprentissage appliqué aux réseaux d'antennes

| Réf | Piste | Priorité | Question visée | État |
| --- | --- | --- | --- | --- |
| A16 | Travaux appliquant l'apprentissage à la calibration de réseaux | 1 | quelqu'un a-t-il déjà répondu à notre question ? | à trouver |
| A17 | Prédiction de dérive et maintenance prédictive de systèmes RF | 2 | axe original et mesurable | à trouver |

---

## 2. Industrie

| Réf | Piste | Ce qu'on en attend | État |
| --- | --- | --- | --- |
| I1 | Kits pédagogiques de réseau à commande de phase, avec leur documentation complète | une architecture réelle entièrement décrite, gratuitement | à trouver |
| I2 | Fiches techniques de circuits de formation de faisceau intégrés | ce qui existe, à quel prix, avec quelles performances | à trouver |
| I3 | Fiches techniques de déphaseurs et d'atténuateurs commandés | composants candidats | à trouver |
| I4 | Notes d'application sur la calibration de réseaux | protocoles éprouvés | à trouver |
| I5 | Documentation de radios logicielles multi-voies cohérentes | option pour la voie numérique | à trouver |

I1 est probablement la source la plus rentable du projet. Certains fabricants
publient des kits pédagogiques complets avec schémas, code et explications
détaillées. Même sans acheter le kit, la documentation seule vaut le temps de
lecture.

---

## 3. Open source

| Réf | Piste | Rôle | État |
| --- | --- | --- | --- |
| O1 | Bibliothèque de traitement de paramètres S | mesure et analyse | à évaluer, commun avec NeuralRFIC |
| O2 | Bibliothèque de pilotage d'instruments | automatisation | à évaluer, commun avec NeuralRFIC |
| O3 | Bibliothèques d'optimisation bayésienne | méthode candidate | à évaluer |
| O4 | Simulateurs électromagnétiques libres | vérification avant simulation propriétaire | à évaluer |
| O5 | Codes ouverts de simulation de réseaux d'antennes | référence de calcul | à évaluer |
| O6 | Projets ouverts de réseaux à commande de phase amateurs | retours d'expérience concrets | à évaluer |
| O7 | Outils de conception de circuits imprimés | antennes imprimées | disponible |

O6 est utile différemment des autres : les projets amateurs documentent souvent
leurs échecs, ce que la littérature académique ne fait jamais. C'est précisément
l'information la plus utile quand on démarre.

---

## 4. Ce que la littérature ne couvre probablement pas

1. Une comparaison chiffrée du **nombre de mesures physiques** nécessaires à
   plusieurs méthodes de calibration, sur le même réseau réel.
2. La durée de validité d'une calibration dans des conditions ordinaires,
   c'est à dire sans enceinte climatique.
3. Une évaluation de ce qu'un montage à faible coût permet réellement de mesurer,
   avec les incertitudes annoncées.
4. Une validation croisée entre un réseau acoustique et un réseau RF, montrant que
   les mêmes algorithmes de calibration fonctionnent sur les deux.

Le point 4 serait une contribution originale et amusante, et il est à notre
portée.

---

## 5. Priorités de lecture

| Ordre | Quoi | Pourquoi maintenant |
| --- | --- | --- |
| 1 | A6, calibration par rotation de phase | méthode centrale, peu exigeante en matériel |
| 2 | A7, calibration par le couplage | pourrait supprimer le besoin de banc de mesure |
| 3 | I1, kits pédagogiques documentés | architecture de référence gratuite |
| 4 | A9, effet statistique des erreurs | justifie quantitativement tout le projet |
| 5 | A1 et A2, fondamentaux | pour ne pas écrire de bêtises |
| 6 | A13, optimisation bayésienne | seulement quand la référence classique est établie |

## 6. Suivi

Chaque source lue produit une fiche dans `research/fiches/`.
