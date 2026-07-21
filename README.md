# Hotel & Restaurant Reviews Scraper + Sentiment Analysis

Ce projet collecte des avis d'hôtels et de restaurants et effectue une analyse de sentiment pour classer chaque commentaire comme positif, négatif ou neutre.

## Description

L'objectif de ce projet est de traiter des avis de voyageurs récupérés depuis TripAdvisor et d'annoter ces avis avec une analyse de sentiment automatique.

Deux scripts principaux sont inclus :

- `sentiment_hotel.py` : analyse les avis d'hôtels et met à jour la base MongoDB avec un champ `analyse_sentiment` dans chaque commentaire.
- `sentiment_restaurant.py` : analyse les avis de restaurants et met à jour la base MongoDB avec un champ `sentiment` dans chaque commentaire.

Le projet inclut également des notebooks Jupyter pour explorer les données :

- `TripAdvisor_Hotel.ipynb`
- `TripAdvisor_restaurants.ipynb`

## Structure du projet

- `hotels.json` : liste d'hôtels récupérés
- `restaurants.json` : liste de restaurants récupérés
- `TripAdvisor_db.reviews_hotels.json` : avis d'hôtels bruts
- `TripAdvisor_db.reviews_hotels(+sentiment).json` : avis d'hôtels enrichis avec l'analyse de sentiment
- `TripAdvisor_db.reviews_restaurants.json` : avis de restaurants bruts
- `TripAdvisor_db.reviews_restaurants(+sentiment).json` : avis de restaurants enrichis avec l'analyse de sentiment
- `sentiment_hotel.py` : script de traitement des avis d'hôtels
- `sentiment_restaurant.py` : script de traitement des avis de restaurants

## Prérequis

1. Python 3.x
2. MongoDB installé et en fonctionnement localement
3. Librairies Python :
   - `pymongo`
   - `nltk`
   - `tqdm`

## Installation des dépendances

```bash
pip install pymongo nltk tqdm
```

Le projet utilise le lexique VADER de NLTK. Le script télécharge automatiquement le package `vader_lexicon` au premier lancement.

## Configuration

Avant d'exécuter les scripts, vérifiez que MongoDB est démarré et accessible via :

- URI : `mongodb://localhost:27017/`
- Base de données : `Imad_Sassi`
- Collections : `Hotels` et `Restaurants`

Les scripts effectuent un test de connexion et un test de modification pour vérifier l'accès à la base.

## Utilisation

### Lancer l'analyse d'hôtels

```bash
python sentiment_hotel.py
```

### Lancer l'analyse de restaurants

```bash
python sentiment_restaurant.py
```

## Fonctionnement

Pour chaque avis, le script :

1. lit le commentaire existant dans MongoDB
2. calcule le score de sentiment avec VADER
3. classe le commentaire en `positif`, `négatif` ou `neutre`
4. met à jour le document dans la collection MongoDB
5. vérifie quelques échantillons pour confirmer la mise à jour

## Points importants

- Les scripts supposent que la structure des documents MongoDB contient un tableau `reviews` avec des champs `commentaire`.
- La clé utilisée pour stocker le résultat de sentiment diffère selon le script :
  - `analyse_sentiment` pour les hôtels
  - `sentiment` pour les restaurants

## Notes

- Ce projet est surtout un prototype d'analyse de sentiment et de traitement de données de commentaires.
- Les notebooks Jupyter permettent d'explorer les avis et de vérifier les résultats de manière interactive.

## Auteur

Ce dépôt est destiné à présenter un exemple de scraping, traitement de données et analyse de sentiment pour des avis d'hôtels et de restaurants.
