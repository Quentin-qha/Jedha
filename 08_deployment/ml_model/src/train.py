import pandas as pd
import numpy as np

from preprocessing import prepare_data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from catboost import CatBoostRegressor
import mlflow
import shutil

import os, warnings
warnings.filterwarnings("ignore", category=UserWarning)

save_path = "/home/app/saved_models/catboost_price_model"
if os.path.exists(save_path):
    shutil.rmtree(save_path)

boolean_columns = ["private_parking_available", "has_gps", "has_air_conditioning", "automatic_car", "has_getaround_connect", "has_speed_regulator"]

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "..", "data", "get_around_pricing_project.csv")

df = prepare_data(data_path, boolean_columns)

feature_target = "rental_price_per_day"
X = df.loc[:, df.columns != feature_target]
y = df[feature_target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ["mileage", "engine_power", *boolean_columns]
categorical_features = ["model_key", "fuel", "car_type"]

EXPERIMENT_NAME="08_deployemet_project"

mlflow.set_experiment(EXPERIMENT_NAME)
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
mlflow.sklearn.autolog(log_models=False)

client = mlflow.tracking.MlflowClient()
run = client.create_run(experiment.experiment_id)

with mlflow.start_run(run_id = run.info.run_id) as run:
    numeric_transformer = Pipeline(
        steps=[
            ('scaler', StandardScaler())
        ])

    categorical_transformer = Pipeline(
        steps=[
            ('encoder', OneHotEncoder(drop='first', handle_unknown='infrequent_if_exist', min_frequency=30))
        ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    params = {'depth': 6, 'l2_leaf_reg': 9, 'learning_rate': 0.08, 'n_estimators': 700}
    model = CatBoostRegressor(**params, random_state=42)

    final_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', model)
    ])

    final_pipeline.fit(X_train, y_train)

    y_pred = final_pipeline.predict(X_test)

    mlflow.set_tag("mlflow.user", "Quentin")
    mlflow.set_tag("mlflow.note.content", "Pipeline CatBoost v0.1 - training sur dataset pricing")
    mlflow.sklearn.log_model(
        sk_model=final_pipeline,
        name="GetAroundPrice",
        registered_model_name="CatBoostRegressorGetAround"
    )
    mlflow.end_run()