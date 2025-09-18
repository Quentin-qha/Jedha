import mlflow
import mlflow.sklearn
import pandas as pd

mlflow.set_tracking_uri("https://qhadata-ml-flow.hf.space/")

model_name = "CatBoostRegressorGetAround"
model_version = "1"
mlflow.sklearn.load_model(f"models:/{model_name}/{model_version}")
model = mlflow.pyfunc.load_model(f"models:/{model_name}/{model_version}")

sample = pd.DataFrame([{
    "mileage": 106054,
    "engine_power": 160,
    "private_parking_available": 0,
    "has_gps": 1,
    "has_air_conditioning": 0,
    "automatic_car": 0,
    "has_getaround_connect": 0,
    "has_speed_regulator": 0,
    "model_key": "Audi",
    "fuel": "diesel",
    "car_type": "estate"
}])

prediction = model.predict(sample)
print("Prix prédit :", round(prediction[0],2))