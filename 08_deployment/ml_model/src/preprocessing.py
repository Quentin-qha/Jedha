import pandas as pd
import numpy as np

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