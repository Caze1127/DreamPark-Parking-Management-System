# Dream Park — Système de gestion de parking

Projet universitaire de programmation orientée objet en Python, réalisé dans le cadre de la **Licence 3 MIASHS — parcours Informatique et SHS**, à l’**Université Toulouse — Jean-Jaurès**.

Dream Park est une application de bureau qui simule le fonctionnement d’un parking : attribution des places, bornes d’entrée et de sortie, gestion des clients et abonnements, prestations de service, livraison de véhicules, statistiques et sauvegarde des données.

## Aperçu de l’interface

Interface modernisée avec un tableau de bord bleu nuit, des actions turquoise et des espaces distincts pour les clients, les voituriers et l’administrateur.

![Tableau de bord de Dream Park](docs/screenshots/tableau-de-bord.png)

![Identification et choix du rôle](docs/screenshots/identification.png)

> Les captures présentent l’interface avec des valeurs de démonstration. Aucune donnée client réelle n’est publiée dans le dépôt.

## Fonctionnalités

### Parking et circulation
- Parking initialisé avec **20 places réparties sur 3 niveaux** ; chaque place possède un numéro, un niveau et des dimensions.
- Recherche d’une place disponible et compatible avec la taille du véhicule.
- **Deux accès physiques simulés** (accès 1 et accès 2), chacun doté de sa propre caméra, borne à tickets, panneau d’affichage et de deux téléporteurs simulés.
- Les deux accès partagent un seul parking : un véhicule peut entrer par une borne et ressortir par l’autre ; les panneaux indiquent le même nombre de places libres.
- Enregistrement de l’accès d’entrée et de sortie dans l’historique des stationnements.

### Clients et abonnements
- Identification d’un abonné par **numéro de carte à 8 chiffres** ou création d’une session de nouveau client.
- Abonnement classique et **Super-abonné** ; modification et résiliation des formules.
- Pour un véhicule stationné, génération d’un ticket comportant une **référence hexadécimale de 6 caractères** à saisir lors de la sortie.
- Contrôle des immatriculations et refus des stationnements actifs en double.

### Services
- Demande de **maintenance**, **entretien** ou **livraison** par les clients abonnés.
- Modification du service demandé, avec saisie d’une heure pour la livraison et utilisation de l’adresse du client.
- Exécution de la livraison depuis un **espace Voiturier** séparé : visualisation des demandes, sélection et confirmation.
- Gestion d’une **prise en charge garantie simulée** lorsque le véhicule d’un Super-abonné ne peut pas être affecté à une place adaptée.

### Administration et statistiques
- Espace Administrateur séparé de l’espace client.
- Statistiques sur les passages, les véhicules, les services utilisés, les places et niveaux, ainsi que les durées de stationnement.
- Export des statistiques aux formats **TXT** et **HTML**.

### Persistance
- Sauvegarde en **JSON** dans `donnees/dreampark.json`.
- Rechargement des clients, véhicules, abonnements, places, placements et historiques au redémarrage.
- Conservation des références de tickets et des numéros d’accès.
- Écriture par fichier temporaire puis remplacement du JSON, afin de limiter les écritures incomplètes.

## Confidentialité des données

Le fichier `donnees/dreampark.json` est créé lors de la première sauvegarde et est ignoré par Git via `.gitignore`. Il peut contenir des noms, adresses, plaques d’immatriculation et numéros de carte : **ne le publiez pas sur GitHub**. La version publique démarre avec un parking vierge.

## Technologies

- **Python 3** (version récente recommandée : 3.10 ou ultérieure).
- **Tkinter** pour l’interface graphique.
- **unittest** et `unittest.mock` pour les tests.
- Modules de la bibliothèque standard : `json`, `pathlib`, `datetime`, `uuid`, `secrets`, `os`, `tempfile`, etc.

Aucune dépendance Python externe n’est nécessaire pour exécuter cette version du projet. Tkinter doit être disponible dans l’installation Python.

## Architecture MVC

Le projet suit une séparation **Modèle — Vue — Contrôleur** :

- **`Class/` — Modèle :** règles du parking et des services, objets métier, statistiques et persistance. Le point d’entrée du programme est `Class/main.py`.
- **`Vue/` — Vue :** fenêtres Tkinter (client, entrée, sortie, services, voiturier, administrateur, statistiques).
- **`Controleur/` — Contrôleur :** `ControleurPrincipal` relie les actions des boutons aux traitements du modèle et à la sauvegarde.
- **`Tests/` — Tests :** scénarios unitaires et d’intégration sans modification du fichier JSON utilisé en production.
- **`donnees/` — Données :** état du parking enregistré localement.

```text
DreamPark/
├── Class/
│   ├── main.py
│   ├── acces.py
│   ├── parking.py
│   ├── place.py
│   ├── placement.py
│   ├── voiture.py
│   ├── client.py
│   ├── abonnement.py
│   ├── voiturier.py
│   ├── administrateur.py
│   ├── sauvegarde.py
│   └── ...
├── Controleur/
│   └── controleur_principal.py
├── Vue/
│   ├── vue_principale.py
│   ├── vue_identification.py
│   ├── vue_voiturier.py
│   ├── vue_administrateur.py
│   └── ...
├── Tests/
│   ├── test_acces.py
│   ├── test_deux_acces.py
│   ├── test_sauvegarde.py
│   └── ...
├── donnees/
│   └── dreampark.json
├── README.md
└── RAPPORT_TESTS.md
```

## Installation et démarrage

1. Récupérer le dossier du projet, en conservant les sous-dossiers `Class`, `Vue`, `Controleur`, `Tests` et `donnees`.
2. Ouvrir un terminal **à la racine `DreamPark`**, pas à l’intérieur de `Class`.
3. Vérifier la version de Python :

```powershell
python --version
```

4. Lancer l’application :

```powershell
python -m Class.main
```

Sous Windows, le lancement fonctionne depuis PowerShell ou le terminal de PyCharm. Si `python` n’est pas reconnu, essayer `py -m Class.main`.

**Important :** ne pas exécuter directement `python Class/main.py`, car le projet utilise des imports relatifs depuis le package `Class`.

## Exemple d’utilisation

**Entrer un véhicule**
1. Depuis l’identification, utiliser une carte existante ou choisir un nouveau client.
2. Cliquer sur « Entrer une voiture ».
3. Sélectionner la **borne 1 ou 2**, saisir l’immatriculation et les dimensions, puis l’offre et le paiement si nécessaire.
4. Valider. L’application affecte une place et affiche un ticket ; **conserver la référence à 6 caractères**.

**Reprendre un véhicule**
1. Cliquer sur « Reprendre une voiture ».
2. Choisir la borne de sortie 1 ou 2.
3. Saisir les **6 caractères de la référence** du ticket (et non le texte complet du ticket).
4. Valider pour libérer la place.

**Demander puis effectuer une livraison**
1. Le client abonné sélectionne le service « livraison » et saisit l’heure souhaitée.
2. Depuis l’identification, ouvrir **« Accès voiturier »**.
3. Sélectionner la demande et confirmer l’exécution. La place est alors libérée et l’opération enregistrée.

**Consulter les statistiques**
1. Depuis l’identification, ouvrir **« Accès administrateur »**.
2. Cliquer sur « Consulter les statistiques ».
3. Actualiser, puis éventuellement exporter en TXT ou en HTML.

## Tests

La suite automatisée contient **205 tests répartis dans 21 fichiers**. Résultat observé sur la version livrée : **205 tests réussis, aucun échec**.

À la racine du projet :

```powershell
python -m unittest discover -s Tests -p "test_*.py" -v
```

Pour vérifier un domaine particulier :

```powershell
python -m unittest Tests.test_deux_acces -v
python -m unittest Tests.test_sauvegarde -v
python -m unittest Tests.test_interface_voiturier -v
```

Le détail des 21 fichiers, le rôle des tests, la méthodologie et les scénarios de vérification manuelle figurent dans **[RAPPORT_TESTS.md](RAPPORT_TESTS.md)** ; une version PDF accompagne également le rendu.

## Limites et choix de simulation

- Les caméras, téléporteurs et bornes sont **modélisés en Python**, sans connexion à un équipement physique.
- Les paiements sont **validés au niveau du programme**, sans transaction bancaire réelle.
- Les espaces Voiturier et Administrateur sont des **accès de démonstration**, sans authentification professionnelle sécurisée.
- L’heure de livraison est une information de demande ; **la livraison n’est pas déclenchée automatiquement** à l’heure indiquée.
- Le pack garanti est **simulé** ; il n’existe pas de réseau de parkings externes piloté par l’application.
- Les exports disponibles sont TXT et HTML ; les autres formats évoqués dans le sujet ne sont pas développés.
- La sauvegarde JSON est locale et ne remplace pas un serveur multi-utilisateur. Les deux accès sont indépendants au niveau des objets mais restent simulés dans une seule application.

## Remise du projet

Le code source, les tests, le fichier JSON et les deux documents d’accompagnement suffisent pour reproduire la démonstration. Les dossiers d’environnement local (`.venv/`, `.idea/`, `__pycache__/`) ne sont pas nécessaires à l’exécution et ne doivent pas être inclus dans un dépôt Git.

---

Projet pédagogique — Dream Park, Université Toulouse — Jean-Jaurès, L3 MIASHS.
