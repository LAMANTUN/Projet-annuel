# 🗺️ Cartographie du Système d'Information (SI) – Département 35

Ce projet permet de visualiser de manière interactive les composants du système d'information :
- Applications hébergées
- Serveurs physiques/virtuels
- Services métiers associés
- Bases de données
- Interfaces entre systèmes

---

## 🚀 Fonctionnalités principales

- Analyse d’impact d’un serveur sur les applications et services métiers
- Visualisation interactive sous forme de "poupée russe" (serveur → applis → services)
- Interface SQL sécurisée (lecture seule) pour exécuter des requêtes personnalisées
- Architecture modulaire avec Django + PostgreSQL en containers Docker

---

## 🧱 Structure technique

- **Backend** : Django 5.x
- **Base de données** : PostgreSQL 15
- **Frontend** : HTML/CSS + JS + Chart.js (treemap)
- **Conteneurisation** : Docker + docker-compose

---

## 🐳 Lancer le projet avec Docker

### 🔁 Prérequis
- Docker Desktop installé (et activé)
- Git (pour cloner le projet)

### ▶️ Démarrage rapide

```bash
# 1. Cloner le projet
git clone https://github.com/moncompte/cartographie-si.git
cd cartographie-si

# 2. Lancer le projet
docker-compose up --build
```

👉 L'application sera accessible sur [http://localhost:8000](http://localhost:8000)

---

## 🛠️ Commandes utiles (dans le conteneur `web`)

```bash
# Accéder au conteneur web
docker-compose exec web bash

# Créer les migrations (si modèles modifiés)
python manage.py makemigrations
python manage.py migrate

# Charger des données d'exemple
python manage.py loaddata test_data_fixture.json
```

---

## 🧪 Interface de test

- **Page d'analyse d'impact** : [http://localhost:8000/](http://localhost:8000/)
- **Interface SQL** (lecture seule) : [http://localhost:8000/sql/](http://localhost:8000/sql/)
- **Visualisation interactive** : [http://localhost:8000/visualisation/](http://localhost:8000/visualisation/)

---

## 📁 Organisation du projet

```bash
.
├── carto_project/           # Projet Django principal
│   ├── carto_app/           # Application métier
│   │   ├── models.py        # Modèles de données (Serveur, Application, etc.)
│   │   ├── views.py         # Vues : impact, SQL, visualisation
│   │   ├── templates/       # Fichiers HTML
│   │   └── urls.py          # Routes de l'app
│   └── settings.py          # Configuration Django
├── test_data_fixture.json   # Jeu de données fictif (fixture)
├── Dockerfile               # Image Docker pour Django
├── docker-compose.yml       # Stack Docker avec PostgreSQL
└── entrypoint.sh            # Script de démarrage pour Docker
```

---

## 🔐 Authentification

Un compte superutilisateur est automatiquement créé :
- **Nom d’utilisateur** : `admin`
- **Mot de passe** : `admin`
- **Email** : `admin@example.com`

---

## 📌 TODO (améliorations futures)

- ✅ Filtres dynamiques dans la visualisation
- ⏳ Vue inversée par *Service métier → Applications → Serveur*
- ⏳ Export CSV / Excel
- ⏳ Ajout des interfaces entre systèmes (API, flux)

---

## 📄 Licence

Projet à but pédagogique – Département d’Ille-et-Vilaine  
Réalisé dans le cadre d’un projet annuel ESGI

