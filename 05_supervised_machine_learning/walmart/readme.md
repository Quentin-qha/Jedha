# 🛒 Walmart Weekly Sales — Predictive Modeling
*Certification Bloc #5 — Data Science Training*

## Project Overview

This project was carried out as part of a machine learning course. The Walmart marketing team requested a model capable of estimating weekly store sales as accurately as possible, in order to better understand the influence of economic indicators and support future marketing campaign planning.

## Dataset

- **Source**: Custom dataset based on a Kaggle competition (provided by the course)
- **Size**: 150 rows × 8 columns (80 usable rows after cleaning)
- **Period**: February 2010 — October 2012
- **Target variable**: `Weekly_Sales`

| Column | Type | Description |
|---|---|---|
| Store | Categorical | Store ID (1–20) |
| Date | DateTime | Week of sales recording |
| Weekly_Sales | Float | Target — weekly sales in $ |
| Holiday_Flag | Binary | 1 = holiday week |
| Temperature | Float | Temperature in °F |
| Fuel_Price | Float | Regional fuel price |
| CPI | Float | Consumer Price Index |
| Unemployment | Float | Unemployment rate |

## Project Structure
```
├── datas/
│   └── Walmart_Store_sales.csv
├── Walmart_project.ipynb
└── README.md
```


## Methodology

### Part 1 — EDA & Preprocessing
- Exploratory analysis with visualizations (distributions, correlations, outliers, temporal analysis)
- Feature engineering from `Date` → `Year`, `Month`, `Day`, `dayOfWeek`
- Conversion of `Temperature` from °F to °C
- Outlier removal using ±3σ rule on `Temperature_C`, `Fuel_Price`, `CPI`, `Unemployment`
- sklearn pipeline: `SimpleImputer` + `StandardScaler` + `OneHotEncoder`

### Part 2 — Baseline Linear Regression
- Train/test split: 80/20 with `random_state=42`
- Evaluation: RMSE and R² on train and test sets
- Coefficient analysis via `.coef_`

### Part 3 — Regularized Models (Bonus: GridSearchCV)
- Ridge and Lasso with `GridSearchCV` over `alpha ∈ [0.1, 1, 10, 100, 500]`
- 5-fold cross-validation
- Coefficient comparison Ridge vs Lasso
- Normalized model on store-centered sales to isolate economic features

## Results

| Model | Test RMSE | Test R² |
|---|---|---|
| Linear Regression | 130,125 $ | 0.96 |
| Ridge (α=0.1) | 137,938 $ | 0.96 |
| Lasso (α=100) | 144,508 $ | 0.96 |

## Key Findings

- **Store identity** is by far the strongest predictor of weekly sales
- **CPI** is the most correlated economic feature with `Weekly_Sales` (r = -0.33)
- Economic features alone explain only **11% of sales variance** (R² = 0.11 on normalized model)
- **`Fuel_Price`** and **`Year`** are the most influential economic drivers
- Multicollinearity between `Fuel_Price` and `Year` (r = 0.81) was detected and mitigated via regularization

---

> 📌 *Project completed by Quentin Haentjens* — on June 24, 2025, as part of my training at Jedha.

