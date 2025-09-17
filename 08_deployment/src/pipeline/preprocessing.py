import pandas as pd
import numpy as np

"""
boolean_columns = ["private_parking_available", "has_gps", "has_air_conditioning", "automatic_car", "has_getaround_connect", "has_speed_regulator"]

for column in boolean_columns:
    df[column] = df[column].map({True: 1, False: 0})


feature_target = "rental_price_per_day"
X = df.loc[:, df.columns != feature_target]
y = df[feature_target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ["mileage", "engine_power", *boolean_columns]
categorical_features = ["model_key", "fuel", "car_type"]"""





# Mes fonctions de nettoyage
def prepare_data(df_url, boolean_columns):
    df = pd.read_csv(df_url)
    df = df.drop(columns=["Unnamed: 0", "winter_tires", "paint_color"])

    df = df[df["mileage"] <= 500_000]

    model_count = df['model_key'].value_counts()
    df['model_key'] = df['model_key'].apply(lambda x: x if model_count[x] > 50 else "other")

    fuel_count = df['fuel'].value_counts()
    df['fuel'] = df['fuel'].apply(lambda x: x if fuel_count[x] > 50 else "other")

    car_type_count = df['car_type'].value_counts()
    df['car_type'] = df['car_type'].apply(lambda x: x if car_type_count[x] > 50 else "other")

    for column in boolean_columns:
        df[column] = df[column].map({True: 1, False: 0})

    return df