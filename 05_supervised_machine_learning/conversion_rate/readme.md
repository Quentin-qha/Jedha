# 🎯 Conversion Rate Prediction
*Certification Bloc #5 — Data Science Training*

## 🎯 Objectif

The goal of this project is to **predict whether a user will convert or not**, based on their behavior and profile information. This task is part of a digital marketing use case, where conversion is a critical KPI for both business performance and UX optimization.

## 🎯 Goal

- **Identify key patterns** in user behavior that drive conversions.
- **Compare classification models** (Logistic Regression, Random Forest, XGBoost).
- Deliver a model that is both **accurate** and **interpretable**.
- Provide **recommendations** for business/UX improvements.

## 🔧 Tech Stack

- **Pandas & NumPy**: For data manipulation, analysis, and handling missing values.
- **Matplotlib & Plotly**: For visualizations during EDA and interpretation of model results.
- **Scikit-learn**: For preprocessing (OneHotEncoding, StandardScaler), modeling (Logistic Regression, Random Forest), evaluation (f1, precision, recall, ROC).
- **XGBoost**: For testing a powerful gradient boosting method.
- **Pipeline & GridSearchCV**: For hyperparameter tuning and model reproducibility.

## 📌 Steps

To reproduce or understand the workflow of this project, follow these steps:

1. **EDA (Exploratory Data Analysis)**:
   - Understand conversion trends.
   - Identify key variables (age, country, new/returning users, etc.)
   - Visual exploration of distributions and correlations.

2. **Preprocessing**:
   - Encoding categorical variables (`country`, `source`, etc.)
   - Scaling numerical features (e.g., `age`).
   - Handling class imbalance if necessary.

3. **Modeling**:
   - Split the data (train/test).
   - Test different models: Logistic Regression, Random Forest, XGBoost.
   - Evaluate models using **f1-score**, **precision**, **recall**, and **ROC-AUC**.

4. **Model Evaluation & Selection**:
   - Use confusion matrix and classification report.
   - Optimize hyperparameters (GridSearchCV).
   - Choose the best performing model.

5. **Interpretation & Recommendations**:
   - Feature importance analysis.
   - Concrete suggestions for marketing or UX based on the most influential factors.

## 🚀 Next Steps

Possible future developments include:

- Try other advanced models: **LightGBM**, **CatBoost**.
- Add SHAP or LIME for **explainability**.
- Deploy the best model into a **Streamlit dashboard**.
- Monitor model performance on real-world or updated datasets.

---

> 📌 *Project completed by Quentin Haentjens* — on June 24, 2025, as part of my training at Jedha.

