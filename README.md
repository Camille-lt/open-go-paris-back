#  Open Go Paris - Backend

<img width="1371" height="712" alt="open-go-paris-dekstop" src="https://github.com/user-attachments/assets/c4be8c72-6f0d-4f2a-abdd-ce9e58299809" />
--> en ligne : https://open-go-paris.vercel.app/
--> le repo front : https://github.com/Camille-lt/open-go-paris

API REST pour l'application **Open Go Paris**, permettant de gérer les réservations d'événements culturels parisiens.

## Stack Technique
* **Framework :** FastAPI (Python)
* **Base de données :** PostgreSQL (hébergé sur Neon.tech)
* **Déploiement :** Render
* **CI/CD :** GitHub Actions (Linter & Tests automatiques)

## Fonctionnalités
* Récupération des données en temps réel via l'API Open Data Paris.
* Gestion du CRUD pour les réservations (POST, GET, DELETE).
* Système de filtrage par catégorie (Théâtre, Concert, Sport, etc.).

## CI/CD & Qualité
Une pipeline **GitHub Actions** est configurée pour garantir la stabilité du code :
* À chaque `push` ou `pull request` sur la branche `main`, le workflow vérifie la validité des dépendances et lance les tests unitaires.
* Permet d'adopter des bonnes pratiques de développement collaboratif.

## Installation locale
1. Cloner le repo.
2. Créer un environnement virtuel : `python -m venv venv`.
3. Installer les dépendances : `pip install -r requirements.txt`.
4. Lancer le serveur : `uvicorn main:app --reload`.
