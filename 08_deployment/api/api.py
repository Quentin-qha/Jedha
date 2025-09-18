import mlflow
import pandas as pd
from fastapi import FastAPI
from typing import List, Any
from pydantic import BaseModel

api = FastAPI(
    title="GetAround Price Prediction API",
    description="API pour prédire le prix de location journalier d'une voiture en fonction de ses caractéristiques.",
    version="1.0.0",
    contact={
        "name": "Quentin Haentjens"
    },
)

mlflow.set_tracking_uri("https://qhadata-ml-flow.hf.space/")

model_name = "CatBoostRegressorGetAround"
model_version = "1"
#mlflow.sklearn.load_model(f"models:/{model_name}/{model_version}")
model = mlflow.pyfunc.load_model(f"models:/{model_name}/{model_version}")

features_col = ["model_key", 
                "mileage", 
                "engine_power",
                "fuel", 
                "car_type",
                "private_parking_available", 
                "has_gps", 
                "has_air_conditioning", 
                "automatic_car", 
                "has_getaround_connect", 
                "has_speed_regulator"]

class InputData(BaseModel):
    input: List[List[Any]]

@api.post(
    "/predict",tags=["Machine Learning"],
    summary="Faire une prédiction de prix",
    description="""
    Cet endpoint prend en entrée les caractéristiques d’une voiture et retourne
    le prix prédit par le modèle **CatBoost Regressor**.
    """
)
def predict_data(data: InputData):
    X = pd.DataFrame(data.input, columns=features_col)
    preds = model.predict(X)
    return {"prediction": preds.tolist()}

@api.get("/", tags=["System"])
def root():
    return {"message": "GetAround API is running"}

@api.get("/health", tags=["System"])
def healthcheck():
    return {"status": "ok"}

@api.get("/model-info", tags=["Model"])
def model_info():
    return {
        "name": "CatBoostRegressorGetAround",
        "version": 1,
        "features": features_col,
        "tracking_uri": "https://qhadata-ml-flow.hf.space/"
    }

@api.get("/example-input", tags=["Help"])
def example_input():
    return {
        "input": [
            ["Audi", 106054, 160, "diesel", "estate", 0, 1, 0, 0, 0, 1]
        ]
    }
