import mlflow
import pandas as pd
from fastapi import FastAPI, Query
from typing import List, Any
from pydantic import BaseModel, Field, validator

api = FastAPI(
    title="GetAround Daily Price Prediction API",
    description="API to predict the daily rental price of a car based on its characteristics.",
    version="1.0.0",
    contact={
        "name": "Quentin Haentjens"
    },
)

mlflow.set_tracking_uri("https://qhadata-ml-flow.hf.space/")

model_name = "CatBoostRegressorGetAround"
model_version = "1"
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

ALLOWED_MODELS = {"Audi", "Citroen", "Renault", "BMW", "Peugeot", "Nissan", "Mitsubishi", "Mercedes", "Volkswagen", "Toyota", "SEAT", "Subaru", "PGO", "Opel", "Ferrari", "other"}
ALLOWED_FUELS = {"diesel", "petrol", "other"}
ALLOWED_CARTYPES = {"estate", "sedan", "suv", "hatchback", "coupe", "other"}

class InputData(BaseModel):
    input: List[List[Any]] = Field(
        example=
            [
                ["Audi", 106054, 160, "diesel", "estate", 0, 1, 0, 0, 0, 1], 
                ["BMW", 106054, 160, "diesel", "suv", 1, 0, 0, 1, 0, 1]
            ]
    )
    @validator("input")
    def validate_input(cls, v):
        for row in v:
            if row[0] not in ALLOWED_MODELS:
                raise ValueError(f"🚨 model_key '{row[0]}' is not supported. Options: {ALLOWED_MODELS}")
            if row[3] not in ALLOWED_FUELS:
                raise ValueError(f"🚨 fuel '{row[3]}' is not supported. Options: {ALLOWED_FUELS}")
            if row[4] not in ALLOWED_CARTYPES:
                raise ValueError(f"🚨 car_type '{row[4]}' is not supported. Options: {ALLOWED_CARTYPES}")
        return v

#Predict via json
@api.post(
    "/predict",
    tags=["Machine Learning"],
    summary="Predict the rental price (€/day) based on the vehicle's characteristics",
    description="""
This endpoint takes a car's characteristics as input and returns
the predicted price using the **CatBoost Regressor** model.

### Expected fields
| Field                       | Type        | Accepted values |
|-----------------------------|-------------|------------------|
| **model_key**               | str         | "Audi", "Citroen", "Renault", "BMW", "Peugeot", "Nissan", "Mitsubishi", "Mercedes", "Volkswagen", "Toyota", "SEAT", "Subaru", "PGO", "Opel", "Ferrari", "other" |
| **mileage**                 | int         | *kilometers driven* |
| **engine_power**            | int         | *horses* |
| **fuel**                    | str         | "diesel", "petrol", "other" |
| **car_type**                | str         | "estate", "sedan", "suv", "hatchback", "coupe", "other" |
| **private_parking_available** | int         | 0 ou 1 |
| **has_gps**                 | int         | 0 ou 1 |
| **has_air_conditioning**    | int         | 0 ou 1 |
| **automatic_car**           | int         | 0 ou 1 |
| **has_getaround_connect**   | int         | 0 ou 1 |
| **has_speed_regulator**     | int         | 0 ou 1 |
    """,
    responses={
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "example": {
                        "prediction": [136.93, 145.21]
                    }
                }
            }
        }
    })
def predict_data(data: InputData):
    X = pd.DataFrame(data.input, columns=features_col)
    preds = model.predict(X)
    return {"prediction": [round(float(p), 2) for p in preds]}

#Predict via url
@api.get(
    "/predict/keys", 
    tags=["Machine Learning"],
    summary="Predict the rental price (€/day) based on the vehicle's characteristics from a custom URL",
    description="""
    This endpoint allows making a prediction by passing the parameters directly in the URL. Here is an example:\n\n
    http://localhost:8000/predict/keys?model_key=Audi&mileage=106054&engine_power=160&fuel=diesel&car_type=estate&private_parking_available=0&has_gps=1&has_air_conditioning=0&automatic_car=0&has_getaround_connect=0&has_speed_regulator=1
    """,
    responses={
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "example": {
                        "prediction": [136.93]
                    }
                }
            }
        }
    })
def predict_with_query(
    model_key: str,
    mileage: int,
    engine_power: int,
    fuel: str,
    car_type: str,
    private_parking_available: int,
    has_gps: int,
    has_air_conditioning: int,
    automatic_car: int,
    has_getaround_connect: int,
    has_speed_regulator: int
):
    X = pd.DataFrame([[
        model_key, mileage, engine_power, fuel, car_type,
        private_parking_available, has_gps, has_air_conditioning,
        automatic_car, has_getaround_connect, has_speed_regulator
    ]], columns=features_col)

    preds = model.predict(X)
    return {"prediction": round(float(preds[0]), 2)}

@api.get(
    "/", 
    tags=["System"],
    responses={
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "example": {
                        "message": "GetAround API is running"
                    }
                }
            }
        }
    })
def root():
    return {"message": "GetAround API is running"}

@api.get(
    "/health",
    tags=["System"],
    summary="Check if the API and the model are accessible (monitoring/CI/CD)",
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "message": f"Hello you, I'm alive", 
                        "status": "ok",
                    }
                }
            }
        }
    })
def healthcheck(name: str = "you"):
    return {
        "message": f"Hello {name}, I'm alive", 
        "status": "ok", 
        }

@api.get(
    "/model-info", 
    tags=["Model"],
    summary="Return the production model metadata (name, version, framework, tracking URI)",
    description="""
    Get more information about the prediction model and its parameters.
    """,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "name": "CatBoostRegressorGetAround",
                        "version": 1,
                        "features": [
                            "model_key",
                            "mileage",
                            "engine_power",
                            "fuel",
                            "car_type",
                            "private_parking_available",
                            "has_gps",
                            "has_air_conditioning",
                            "automatic_car",
                            "has_getaround_connect",
                            "has_speed_regulator"
                        ],
                        "tracking_uri": "https://qhadata-ml-flow.hf.space/"
                    }
                }
            }
        }
    })
def model_info():
    return {
        "name": "CatBoostRegressorGetAround",
        "version": 1,
        "features": features_col,
        "tracking_uri": "https://qhadata-ml-flow.hf.space/"
    }

@api.get(
    "/example-input",
    tags=["Help"], 
    description="Example input to understand how to use the prediction model.",
    responses={
        200: {
            "description": "Successful input",
            "content": {
                "application/json": {
                    "example": {
                        "input": [
                            ["Audi", 106054, 160, "diesel", "estate", 0, 1, 0, 0, 0, 1], 
                            ["BMW", 106054, 160, "diesel", "suv", 1, 0, 0, 1, 0, 1]
                        ]
                    }
                }
            }
        }
    })
def example_input():
    return {
        "input": [
            ["Audi", 106054, 160, "diesel", "estate", 0, 1, 0, 0, 0, 1], 
            ["BMW", 106054, 160, "diesel", "suv", 1, 0, 0, 1, 0, 1]
        ]
    }
