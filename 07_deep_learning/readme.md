# 📱 AT&T Spam Detector – Deep Learning Project

## 🎯 Introduction
Ce projet a été réalisé dans le cadre de la certification en **Data Science / Deep Learning**.  
L’objectif est de construire un modèle de classification automatique pour distinguer les **SMS normaux (ham)** des **SMS indésirables (spam)**.

Les SMS frauduleux représentent une menace réelle : perte de confiance, risques de phishing, et impacts financiers pour les utilisateurs et les opérateurs.  
L’enjeu est de proposer une **solution robuste, efficace et exploitable en production**.

## ❓ Pourquoi ce projet ?
- **Problème métier** : AT&T, comme tout opérateur télécom, doit protéger ses utilisateurs des SMS frauduleux.  
- **Impact attendu** : réduire drastiquement le nombre de spams reçus, limiter les faux positifs, améliorer l’expérience client.  
- **Approche pédagogique** : démontrer l’application de techniques de **Deep Learning** sur un problème concret de NLP (Natural Language Processing).

## 👥 Pour qui ?
- **AT&T et les opérateurs télécoms** : intégrer un système de filtrage automatique.  
- **Les utilisateurs finaux** : bénéficier d’une protection renforcée contre les spams.  
- **Les data scientists** : exemple d’étude de cas NLP appliqué au domaine des télécommunications.

## 🛠️ Étapes principales du projet
1. **Exploration des données (EDA)**  
   - Analyse des colonnes, valeurs manquantes, distribution ham/spam.  
   - Observation des longueurs de SMS.  

2. **Prétraitement du texte**  
   - Mise en minuscules, suppression des caractères parasites.  
   - Remplacement des patterns par des tokens `[URL]`, `[MAIL]`, `[NUM]`, `[TEL]`, `[MONEY]`, `[EMOJI]`.  
   - Nettoyage des espaces et normalisation.  

3. **Split des données**  
   - 80% train, 10% validation, 10% test.  
   - Split stratifié pour conserver l’équilibre des classes.  

4. **Modélisation Deep Learning**  
   - **LSTM avec embeddings** (entraînement from scratch).  
   - **BERT (Tiny/Small)** en transfert learning (fine-tuning partiel).  

5. **Évaluation et choix du seuil**  
   - Métriques : F1, ROC-AUC, PR-AUC.  
   - Optimisation du seuil de classification (Youden, F1-max).  
   - Matrices de confusion et courbes ROC/PR.  

6. **Analyse des erreurs**  
   - Faux positifs : promotions légitimes proches du spam.  
   - Faux négatifs : spams très courts et cryptiques.  

7. **Comparaison et storytelling**  
   - LSTM surpasse BERT sur ce dataset (petit et spécialisé).  
   - Discussion sur l’adéquation modèle/données.  

8. **Déploiement**  
   - Sauvegarde du modèle, tokenizer et config (seuil).  
   - Fonction `predict_sms()` pour inférence en production.  

## 📊 Résultats

| Modèle      | Accuracy | F1-score | ROC-AUC | PR-AUC |
|-------------|----------|----------|---------|--------|
| **LSTM**    | 99.1%    | 0.981    | 0.995   | 0.987  |
| **BERT-Small** | 98.4% | 0.966    | 0.995   | 0.977  |

✅ **Le LSTM est retenu comme meilleur modèle** dans ce contexte.  


## 🧾 Analyse des performances
- **Pourquoi LSTM > BERT ici ?**
  - Dataset réduit (~5k SMS) → pas suffisant pour exploiter toute la puissance de BERT.  
  - SMS très courts → LSTM gère bien les séquences brèves.  
  - BERT-Tiny/Small = versions allégées, moins performantes qu’un DistilBERT/Base.  
  - Prétraitement spécialisé (`[URL]`, `[NUM]`, etc.) favorise LSTM.  


## 🚀 Perspectives
- **Augmentation du dataset** (nouveaux SMS, data augmentation).  
- **Transfert learning avancé** : DistilBERT ou BERT-Base.  
- **Adaptation multilingue** : filtrer les SMS en français, espagnol, portugais…  
- **Pipeline hybride** : combinaison Deep Learning + règles simples (regex).  
- **Monitoring en production** : suivi hebdomadaire de PR-AUC et des taux de faux positifs.

---

> 📌 *Project completed by Quentin Haentjens* — on Août 24, 2025, as part of my training at Jedha.
