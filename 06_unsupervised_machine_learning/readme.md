# 🛍️ Product Description Clustering & Recommendation System
*Certification Bloc #6 — Data Science Training*

## 🎯 Objectif

Ce projet a pour but d'exploiter les descriptions textuelles de produits afin de :
- Regrouper automatiquement les articles aux descriptions similaires (**clustering**),
- Identifier les **thématiques latentes** dans le catalogue,
- Construire un **système de recommandation** basé sur le contenu (descriptions).

Il s'agit d'une solution légère et interprétable permettant de mieux naviguer dans un catalogue produit sans supervision.

## 🎯 Goal

This project uses **NLP and unsupervised learning** to:
- Automatically cluster similar products using textual descriptions,
- Extract and visualize **latent semantic topics** (via LSA),
- Provide a **recommendation system** that suggests similar products based on clustering.

## 🔧 Tech Stack

- **Spacy & regex**: For advanced text preprocessing: tokenization, lemmatization, and cleaning HTML/symbols.
- **TF-IDF**: Converts text descriptions into numerical vectors based on term importance across the corpus.
- **TruncatedSVD (LSA)**: Performs dimensionality reduction and extracts latent semantic topics from the TF-IDF matrix.
- **KMeans & DBSCAN**: Unsupervised clustering algorithms used to group similar product descriptions.
- **matplotlib, seaborn & wordcloud**: For data visualization: plots, cluster distributions, and wordclouds to interpret clusters/topics.
- **Python + input() CLI**: Simple command-line interface to allow users to request product recommendations interactively.

## 📌 Steps

To reproduce or understand the workflow of this project, follow these steps:

1. **Exploratory Data Analysis (EDA)**
   - Validation du dataset (500 produits, pas de valeurs manquantes)
   - Analyse de la structure des colonnes (`id`, `description`)

2. **NLP Preprocessing**
   - Nettoyage des descriptions : suppression HTML, ponctuation, mise en minuscules
   - Lemmatisation avec spaCy
   - Suppression des stopwords et des termes non informatifs
   - Texte final stocké dans la colonne `nlp_ready`

3. **TF-IDF + Latent Semantic Analysis (LSA)**
   - Vectorisation avec `TfidfVectorizer`
   - Réduction de dimension avec `TruncatedSVD` (37 composantes ≈ 70% de variance)
   - Interprétation des topics par Wordclouds

4. **Clustering**
   - **KMeans** : testé pour différents `k`, silhouette score ~0.15
   - **DBSCAN** :
      - Distance cosinus + tuning `eps` et `min_samples`
      - 20 clusters + 1 cluster `-1` (outliers)
      - Clusters plus thématiques → DBSCAN retenu

5. **Recommender System**
   - Création d'une fonction `find_similar_items(item_id)`
   - Utilise les clusters DBSCAN pour suggérer 5 produits similaires
   - Interface CLI via `input()`

## 🚀 Next Steps

This project lays the foundation for deeper and more advanced analyses of the marketplace. Possible future developments include:

- Ajouter un moteur **hybride** (cluster + similarité vectorielle)
- Intégrer des **informations enrichies** dans la recommandation (nom, image, lien)
- Tester des **embeddings modernes** : Word2Vec, FastText, BERT
- Créer une **interface web** (ex: Streamlit) pour rendre l’exploration interactive
- Ajouter une visualisation 2D des clusters (PCA ou t-SNE)

---

> 📌 *Project completed by Quentin Haentjens* — on July 30, 2025, as part of my training at Jedha.

