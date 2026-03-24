# Application Gestion de Produits - CI/CD & Qualité

[![Sonarcloud Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=Boitapain_tp_tests&metric=alert_status)](https://sonarcloud.io/dashboard?id=Boitapain_tp_tests)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Boitapain_tp_tests&metric=coverage)](https://sonarcloud.io/dashboard?id=Boitapain_tp_tests)

Cette application est une API CRUD développée en Python (via **FastAPI**) permettant de gérer des produits pour une boutique en ligne. Ce projet intègre les meilleures pratiques DevOps : tests unitaires, mesure de la couverture, analyse statique et complexité, ainsi que l'intégration à des pipelines CI/CD (GitHub Actions, Jenkins) et l'intégration continue de la qualité avec SonarQube.

## Prérequis

- Python 3.9+
- Pip (gestionnaire de paquets)

## Installation et Utilisation Locale

1. **Cloner le projet** ou s'y positionner.
2. **Créer et activer un environnement virtuel** (recommandé) :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
4. **Lancer l'application** :
   ```bash
   python3 -m uvicorn app.main:app --reload
   ```

## Lancement avec Docker

Vous pouvez également lancer l'application dans un conteneur Docker.

1. **Lancer avec Docker Compose** :
   ```bash
   docker compose up --build
   ```
2. **Accéder à l'application** : `http://localhost:8000/docs`

## Documentation de l'API CRUD

Une fois l'application lancée, une interface d'utilisation interactive et complète de l'API (Swagger UI) est générée automatiquement et accessible ici :  
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

Vous pouvez y tester toutes les fonctionnalités CRUD (Créer, Lire, Mettre à jour, Supprimer) des produits.

Un produit possède les attributs suivants:
* `id` : entier (généré automatiquement)
* `nom` : chaîne de caractères
* `description` : chaîne de caractères (optionnelle)
* `prix` : nombre à virgule flottante
* `quantite_stock` : entier

## Qualité du Code et Tests

### Exécuter les tests et mesurer la couverture

Les tests sont écrits avec `pytest`. Le plugin `pytest-cov` est utilisé pour la couverture (génération d'un rapport XML pour SonarQube).

```bash
pytest --cov=app --cov-report=term-missing --cov-report=xml
```
*Nous garantissons une couverture de test >= 80%. Actuellement fixée à **100%**.*

### Mesurer la complexité cyclomatique

Nous utilisons **Radon** pour évaluer la complexité du code source.
```bash
radon cc app -s -a
```
*La complexité moyenne de l'application est **A** (très maintenable).*

## Intégration CI/CD et SonarQube

Le projet est pré-configuré pour être déployé sur des pipelines de CI/CD et analysé par SonarQube.

### SonarQube

Le fichier `sonar-project.properties` situé à la racine du projet contient la configuration pour l'intégration SonarQube.  
Lors de l'analyse, SonarQube récupère les résultats des tests (`coverage.xml`), identifie les *Bugs et vulnérabilités*, ainsi que les *Code Smells*.

### GitHub Actions

Le fichier `.github/workflows/ci.yml` orchestre un pipeline automatisé à chaque push ou pull request :
1. **Tests & Couverture** : Installe les dépendances, exécute les tests, génère le rapport de couverture et évalue la complexité.
2. **SonarQube Scan** : Envoie le rapport de couverture et procède à l'analyse sur le serveur Sonar (nécessite de configurer les secrets GitHub `SONAR_TOKEN`).

