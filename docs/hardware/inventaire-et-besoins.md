# Matériel et moyens de mesure

- Statut : à compléter, l'environnement de mesure est le point critique
- Dernière revue : 2026-08-21

---

## 1. Ce qui décide du projet

Dans ce projet, la contrainte principale n'est ni le budget ni les composants,
c'est **la capacité à mesurer un diagramme de rayonnement dans un environnement
ordinaire**.

Trois questions, dans cet ordre :

1. Peut-on mesurer une puissance reçue de façon reproductible ?
2. Peut-on la mesurer à plusieurs angles, avec un positionnement précis ?
3. Les réflexions de la pièce sont-elles assez faibles pour ne pas masquer le
   phénomène ?

Si la réponse à la troisième question est non, le projet doit changer de stratégie,
et c'est mieux de le savoir tout de suite.

## 2. Inventaire

| Élément | Modèle | Caractéristiques à relever | Rôle |
| --- | --- | --- | --- |
| Analyseur de réseau vectoriel | à compléter | plage, nombre d'accès, mesure de phase entre accès | mesure des voies et du couplage |
| Oscilloscope | à compléter | bande passante, voies | mesure temporelle, cohérence |
| Générateur | à compléter | fréquence maximale, sorties multiples | source |
| Radio logicielle | à compléter, peut-être absente | nombre de voies cohérentes | option numérique |
| Carte FPGA | DE1-SoC et carte secondaire | ressources, entrées sorties | seulement si formation de faisceau numérique |
| Microcontrôleur | STM32, ESP32 | interfaces de commande, temporisateurs | pilotage des déphaseurs, positionneur |
| Moteur pas à pas et pilote | à acquérir probablement | résolution angulaire | rotation du réseau pour la mesure |
| Absorbants | probablement absents | efficacité, quantité | réduction des réflexions |

Le positionneur angulaire est un point souvent sous-estimé. Mesurer un diagramme
demande de tourner le réseau ou la sonde par pas réguliers, plusieurs dizaines de
fois, de façon reproductible. Le faire à la main est possible pour quelques points,
pas pour un diagramme complet, et l'opérateur qui se penche sur le montage modifie
lui-même la mesure.

Fabriquer un positionneur simple avec un moteur pas à pas et un microcontrôleur est
un sous-projet accessible et très utile. Il servirait aussi à NeuralRFIC.

## 3. Le problème des réflexions

Dans une pièce ordinaire, le signal reçu est la somme du trajet direct et de
plusieurs échos. L'effet peut atteindre plusieurs décibels, c'est à dire du même
ordre que ce qu'on mesure.

Moyens d'atténuation, du moins cher au plus cher :

| Moyen | Effet attendu | Coût |
| --- | --- | --- |
| Éloigner le montage des murs et du sol | modéré | nul |
| Mesures différentielles, avec et sans le réseau alimenté | bon sur les échos stables | nul |
| Moyennage sur plusieurs positions | modéré | nul, mais long |
| Absorbants sur les surfaces principales | bon | modéré |
| Fenêtrage temporel, si l'instrument le permet | très bon, sépare le trajet direct des échos | nul si la fonction existe |
| Chambre anéchoïque | excellent | hors de portée |

La ligne "fenêtrage temporel" mérite d'être vérifiée en priorité. Certains
analyseurs de réseau permettent de passer dans le domaine temporel et d'isoler le
trajet direct des réflexions plus tardives. Si cette fonction est disponible, elle
résout une grande partie du problème sans dépenser un euro.

## 4. La voie acoustique

Si l'environnement de mesure RF s'avère mauvais, un réseau à ultrasons résout
presque tous ces problèmes.

| Aspect | Réseau RF à 2,4 GHz | Réseau acoustique à 40 kHz |
| --- | --- | --- |
| Longueur d'onde | 12,5 cm | environ 8,6 mm |
| Espacement à demi-longueur d'onde | 6,25 cm | environ 4,3 mm |
| Coût par élément | modéré à élevé | très faible |
| Génération du déphasage | composant dédié ou numérique | directement numérique, la fréquence est basse |
| Mesure | délicate | un microphone suffit |
| Réflexions | difficiles à maîtriser | plus faciles, matériaux absorbants courants |
| Réalisme du sujet | direct | analogie, à expliquer |

L'écart de longueur d'onde est intéressant : à 40 kHz, les éléments doivent être
espacés de quelques millimètres, ce qui est mécaniquement contraignant avec des
transducteurs de taille standard. Il faudrait donc accepter un espacement supérieur
à la demi-longueur d'onde, et donc des faisceaux parasites. C'est une contrainte
réelle, qui peut au demeurant devenir un objet d'étude à part entière.

Une alternative consiste à descendre en fréquence, vers l'audible, où les
haut-parleurs sont plus faciles à espacer correctement, au prix d'un réseau
physiquement plus grand.

Ces éléments doivent être chiffrés avant de choisir cette voie. Elle est
prometteuse mais pas gratuite.

## 5. Ce qui manque probablement

| Besoin | Contournement | Coût si achat |
| --- | --- | --- |
| Positionneur angulaire | mesure manuelle sur quelques points | faible, fabrication possible |
| Absorbants | éloignement, fenêtrage temporel, mesures différentielles | modéré |
| Déphaseurs commandés | commutation de lignes, ou voie numérique | à chiffrer |
| Voies de réception cohérentes | rester en analogique | élevé |
| Antennes identiques | fabrication sur circuit imprimé | faible en série |

## 6. Sécurité et réglementation

- Puissances très faibles, sans risque.
- Fréquences choisies dans des bandes libres.
- Les mesures rayonnées restent locales et de très faible puissance.
- Pour la voie acoustique, attention à la puissance sonore si l'on descend dans
  l'audible.
