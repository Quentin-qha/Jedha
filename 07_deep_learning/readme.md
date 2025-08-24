# 📱 AT&T Spam Detector – Deep Learning Project

## 🎯 Introduction
This project was carried out as part of the **Data Science / Deep Learning certification**.  
The objective is to build an automatic classification model to distinguish between **normal SMS (ham)** and **unwanted SMS (spam)**.

Fraudulent SMS represent a real threat: loss of trust, phishing risks, and financial impact for users and operators.  
The challenge is to propose a **robust, efficient, and production-ready solution**.

## ❓ Why this project?
- **Business problem**: AT&T, like any telecom operator, must protect its users from fraudulent SMS.  
- **Expected impact**: drastically reduce the number of spam received, limit false positives, and improve customer experience.  
- **Educational approach**: demonstrate the application of **Deep Learning techniques** on a concrete NLP (Natural Language Processing) problem.

## 👥 For whom?
- **AT&T and telecom operators**: integrate an automatic SMS filtering system.  
- **End users**: benefit from enhanced protection against spam.  
- **Data scientists**: a case study of NLP applied to the telecommunications domain.  

## 🛠️ Main project steps
1. **Exploratory Data Analysis (EDA)**  
   - Analysis of columns, missing values, ham/spam distribution.  
   - Observation of SMS length distribution.  

2. **Text preprocessing**  
   - Lowercasing, removal of noisy characters.  
   - Replacement of patterns by tokens `[URL]`, `[MAIL]`, `[NUM]`, `[TEL]`, `[MONEY]`, `[EMOJI]`.  
   - Cleaning of extra spaces and normalization.  

3. **Data splitting**  
   - 80% train, 10% validation, 10% test.  
   - Stratified split to preserve class balance.  

4. **Deep Learning modeling**  
   - **LSTM with embeddings** (trained from scratch).  
   - **BERT (Tiny/Small)** with transfer learning (partial fine-tuning).  

5. **Evaluation and threshold tuning**  
   - Metrics: F1, ROC-AUC, PR-AUC.  
   - Optimization of the decision threshold (Youden, F1-max).  
   - Confusion matrices and ROC/PR curves.  

6. **Error analysis**  
   - False positives: legitimate promotions close to spam.  
   - False negatives: very short and cryptic spam.  

7. **Comparison and storytelling**  
   - LSTM outperforms BERT on this small and specialized dataset.  
   - Discussion on model/data adequacy.  

8. **Deployment**  
   - Saving the model, tokenizer, and config (threshold).  
   - Function `predict_sms()` for production inference.  

## 📊 Results

| Model        | Accuracy | F1-score | ROC-AUC | PR-AUC |
|--------------|----------|----------|---------|--------|
| **LSTM**     | 99.1%    | 0.981    | 0.995   | 0.987  |
| **BERT-Small** | 98.4%  | 0.966    | 0.995   | 0.977  |

✅ **The LSTM is retained as the best model** in this context.  

## 🧾 Performance analysis
- **Why LSTM > BERT here?**
  - Reduced dataset (~5k SMS) → not enough to leverage BERT’s full potential.  
  - Very short SMS → LSTM handles short sequences effectively.  
  - BERT-Tiny/Small = lightweight versions, less powerful than DistilBERT/Base.  
  - Specialized preprocessing (`[URL]`, `[NUM]`, etc.) favors LSTM.  

## 🚀 Perspectives
- **Dataset augmentation** (new SMS, data augmentation).  
- **Advanced transfer learning**: DistilBERT or BERT-Base.  
- **Multilingual adaptation**: filter SMS in French, Spanish, Portuguese, etc.  
- **Hybrid pipeline**: combine Deep Learning + simple rules (regex).  
- **Production monitoring**: weekly tracking of PR-AUC and false positive rates.  

---

> 📌 *Project completed by Quentin Haentjens* — on August 24, 2025, as part of my training at Jedha.
