# 🚗 GetAround Pricing Optimization
*Certification Block #8 — Data Science Training*

## Introduction
GetAround is the Airbnb of cars: a platform that allows peer-to-peer car rentals for a few hours or several days.  
As with any mobility company, handling late returns and setting rental prices are critical challenges, both for car owners and for customers.

## 🎯 Project Objectives
This project has two main goals:

1. **Improve the user experience** by reducing conflicts caused by late returns through an analysis of time buffers between two rentals.  
2. **Optimize owners’ revenues** by providing a Machine Learning model capable of predicting a relevant daily rental price based on car characteristics.  

## 👥 Target Audience
This project is designed for:

- **GetAround’s product and data teams**, who need to balance reducing conflicts with maximizing revenues.  
- **Car owners**, who want a better estimation of their vehicle’s daily rental price.  
- **Students and Data Science professionals**, who want to understand how to set up a complete ML workflow from EDA to deployment (Streamlit + API + MLflow).  

## 📌 Main Steps
**1. Exploratory Data Analysis (EDA)**
- Clean and prepare the dataset provided by GetAround.  
- Identify the distribution of late and early returns.  
- Analyze the impact of check-in mode (mobile vs connect).  
- Assess the risk of conflicts between two consecutive rentals.  
- Estimate potential revenue loss caused by delays.  

**2. Dashboard Construction (Streamlit)**
- Build interactive visualizations (histograms, plots, pie charts).  
- Show the frequency and severity of late returns.  
- Demonstrate the effect of time buffers on conflict risk.  
- Simulate the cost of overly long buffers in terms of lost revenue.  
- Deploy the dashboard online via Hugging Face Spaces.  

**3. ML Model Training (CatBoost + MLflow)**
- Define explanatory variables (mileage, engine power, fuel type, etc.).  
- Build a preprocessing pipeline (encoding, scaling).  
- Train a **CatBoost Regressor** to predict the daily rental price.  
- Evaluate performance (RMSE, MAE, R², MAPE).  
- Version and log experiments with **MLflow** (parameters, metrics, models).  

**4. API Deployment (FastAPI)**
- Create a `POST /predict` endpoint to expose the model.  
- Add useful endpoints: `/health`, `/model-info`, `/example-input`.  
- Document the API with Swagger UI (available by default at `/docs`).  
- Dockerize the API for portable deployment.  
- Test predictions with `curl` or `requests`.  

**5. Online Deployment on Hugging Face**
- Deploy the FastAPI on Hugging Face Spaces.  
- Deploy the Streamlit dashboard on a separate Space.  
- Host the MLflow UI online for experiment tracking.  
- Ensure all services are publicly accessible:  
  - API → https://qhadata-api-getaround-pricing.hf.space/  
  - Dashboard → https://qhadata-streamlit-getaround.hf.space/  
  - MLflow UI → https://qhadata-ml-flow.hf.space/ 

## 🧪 Testing the Model via the API
Run the following command in your terminal: 
```bash
curl -X POST "https://qhadata-api-getaround-pricing.hf.space/predict" \
    -H "Content-Type: application/json" \
    -d '{
      "input": [
        ["Audi", 106054, 160, "diesel", "estate", 0, 1, 0, 0, 0, 1],
        ["BMW", 85000, 150, "petrol", "suv", 1, 0, 1, 1, 0, 1]
      ]
    }'
```
Or directly via URL:
```
https://qhadata-api-getaround-pricing.hf.space/predict/keys?model_key=Audi&mileage=106054&engine_power=160&fuel=diesel&car_type=estate&private_parking_available=0&has_gps=1&has_air_conditioning=0&automatic_car=0&has_getaround_connect=0&has_speed_regulator=1
```

## 🏗️ How It Works
```
                    ┌─────────────────────┐
                    │     Dataset CSV     │
                    │ (getaround_pricing) │
                    └─-────────┬─────────-┘
                               │
                               ▼
                   ┌──────────────────────┐
                   │     Preprocessing    │
                   │ (cleaning, encoding) │
                   └───────────┬──────────┘
                               │
                               ▼
                   ┌─────────────────────┐
                   │   Training MLflow   │
                   │  CatBoost Regressor │
                   └──────────┬──────────┘
                              │
              ┌───────────────┴────────────────┐
              │                                │
              ▼                                ▼
     ┌──────────────────┐            ┌───────────────────┐
     │ MLflow Tracking  │            │   FastAPI API     │
     │  (experiments,   │            │ /predict endpoint │
     │  model registry) │            │ Swagger /docs     │
     └─────────┬────────┘            └─────────┬─────────┘
               │                               │
               ▼                               ▼
     ┌──────────────────┐            ┌────────────────────┐
     │     Artifacts    │            │ Streamlit Dashboard│
     │  (saved models)  │            │   Visualization    │
     └──────────────────┘            └────────────────────┘

```

## 🛠️ Tech Stack

### 🔹 Languages & Frameworks
- **Python 3.12** : main programming language  
- **FastAPI** : prediction API development  
- **Streamlit** : interactive dashboard development  
- **CatBoost** : regression algorithm for price prediction  
- **scikit-learn** : preprocessing, pipelines, and evaluation metrics  
- **MLflow** : experiment tracking, model logging, and versioning  

### 🔹 Containerization & Deployment
- **Docker** : packaging services (API, MLflow, Streamlit)  
- **Hugging Face Spaces** : online hosting for API, dashboard, and MLflow  

### 🔹 Visualization & Monitoring
- **Plotly** : exploratory data visualization  
- **Swagger UI** (auto-generated by FastAPI) : API documentation and testing  

## 🖥️ Commands to Run Locally
### 1. Clone the repository
```bash
git clone https://github.com/Quentin-qha/Jedha.git
```

### 2. Start streamlit
```bash
cd 08_deployment/streamlit_app
docker build -t streamlit-getaround
docker run -p 7860:7860 streamlit-getaround
```

### 3. Launch ml logs to mlflow
```bash
cd 08_deployment/ml_model
docker build -t mlflow-server -f Dockerfile.server .
docker build -t mlflow-project -f Dockerfile.project .
mlflow run .
```

### 4. Lancer l'api
```bash
cd 08_deployment/api
docker build -t api-getaround-price-predict .
docker run -p 8000:8000 --env-file secret.sh api-getaround-price-predict # Contains AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, ARTIFACT_ROOT
```

## 🚀 Next Steps

- [ ] **API Robustness**
  - Add custom error handling with FastAPI.  
  - Limit input size to prevent misuse or abuse.  
  - Implement caching to speed up repeated predictions.  

- [ ] **Streamlit Dashboard**
  - Add more interactive filters (date range, vehicle type, city).  
  - Compare multiple buffer scenarios in real time.  
  - Export results (CSV, PDF).  

- [ ] **Deployment & CI/CD**
  - Implement a CI/CD pipeline (GitHub Actions).  
  - Deploy the API and dashboard on a cloud provider (AWS, GCP, Azure).  
  - Monitor performance with Prometheus + Grafana.  

- [ ] **MLflow**
  - Add a persistent database to store model runs (currently cached).  
  - Save and compare multiple model versions.  

- [ ] **User Experience**
  - Create more detailed technical documentation.  
  - Add a step-by-step tutorial to test the API with `curl` or Python.  
  - Provide an interactive architecture diagram.  

---

> 📌 *Project completed by Quentin Haentjens* — on Septembre 21, 2025, as part of my training at Jedha.