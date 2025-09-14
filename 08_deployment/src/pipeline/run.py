import pandas as pd
import numpy as np

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
#mlflow.log_artifact("/ml-trainer/data/get_around_pricing_project.csv", artifact_path="dataset")
df = pd.read_csv("/ml-trainer/data/get_around_pricing_project.csv")

model_count = df['model_key'].value_counts()
df['model_key'] = df['model_key'].apply(lambda x: x if model_count[x] > 50 else "other")
fuel_count = df['fuel'].value_counts()
df['fuel'] = df['fuel'].apply(lambda x: x if fuel_count[x] > 50 else "other")
car_type_count = df['car_type'].value_counts()
df['car_type'] = df['car_type'].apply(lambda x: x if car_type_count[x] > 50 else "other")
df = df[df["mileage"] <= 500_000]
df = df.drop(columns=["Unnamed: 0", "winter_tires", "paint_color"])

boolean_columns = ["private_parking_available", "has_gps", "has_air_conditioning", "automatic_car", "has_getaround_connect", "has_speed_regulator"]

for column in boolean_columns:
    df[column] = df[column].map({True: 1, False: 0})


feature_target = "rental_price_per_day"
X = df.loc[:, df.columns != feature_target]
y = df[feature_target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ["mileage", "engine_power", *boolean_columns]
categorical_features = ["model_key", "fuel", "car_type"]

# Set your variables for your environment
EXPERIMENT_NAME="08_deployemet_project"

# Set tracking URI to your Hugging Face application
#mlflow.set_tracking_uri(os.environ["APP_URI"])
#mlflow.set_tracking_uri("https://huggingface.co/spaces/qhaData/ml-flow")
mlflow.set_tracking_uri("https://qhadata-ml-flow.hf.space")


# Set experiment's info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Call mlflow autolog
mlflow.sklearn.autolog()

with mlflow.start_run(experiment_id = experiment.experiment_id):
    numeric_transformer = Pipeline(
        steps=[
            ('scaler', StandardScaler()) # TESTER VS ROBUST SCALER EN GRID SEARCH VOIR CE QUI IMPACT LE MIEUX
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

    clean_params = {'depth': 6, 'l2_leaf_reg': 9, 'learning_rate': 0.08, 'n_estimators': 700}

    final_model = CatBoostRegressor(**clean_params, random_state=42)

    final_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', final_model)
    ])
    final_pipeline.fit(X_train, y_train)

    y_pred = final_pipeline.predict(X_test)

    print("RMSE :", root_mean_squared_error(y_test, y_pred))
    print("MAE :", mean_absolute_error(y_test, y_pred))
    print("R² :", r2_score(y_test, y_pred))

    mape = mean_absolute_percentage_error(y_test, y_pred)
    print("MAPE :", mape)

    #mlflow.sklearn.save_model(
     #   sk_model=final_pipeline,
      #  path=save_path,
      #  input_example=X_train.iloc[0:1]
    #)
    #mlflow.log_metric("rmse", root_mean_squared_error(y_test, y_pred))
    #mlflow.log_metric("mae", mean_absolute_error(y_test, y_pred))
    #mlflow.log_metric("r2", r2_score(y_test, y_pred))
    #mlflow.log_metric("mape", mean_absolute_percentage_error(y_test, y_pred))
    #mlflow.sklearn.log_model(
    #    sk_model=final_pipeline,
    #    artifact_path="CatBoostRegressor",
    #    registered_model_name="catboost_price_model"
    #)
    mlflow.set_tag("mlflow.user", "Quentin")
    mlflow.set_tag("mlflow.note.content", "Pipeline CatBoost v0.1 - training sur dataset pricing")
    #mlflow.log_params(clean_params)
    mlflow.end_run()