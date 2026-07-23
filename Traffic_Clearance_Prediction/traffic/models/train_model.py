"""
train_model.py
---------------
Trains a Random Forest Regressor to predict clearance_time,
compares it against the baseline formula, and saves the trained model.
"""

import sys
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "preprocessing"))
from feature_engineering import add_features, encode_traffic_level
from data_cleaning import clean_data

sys.path.append(os.path.dirname(__file__))
from baseline_math_model import calculate_clearance_time

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "clearance_train.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "traffic_model.pkl")

FEATURE_COLUMNS = [
    "num_vehicles", "avg_speed", "road_length", "signal_time",
    "arrival_rate", "flow_rate", "density", "speed_m_s", "traffic_level_encoded"
]
TARGET_COLUMN = "clearance_time"


def load_and_prepare_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df = clean_data(df)
    df = add_features(df)
    df = encode_traffic_level(df)
    return df


def train_and_evaluate():
    df = load_and_prepare_data()

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    print("=== ML Model Performance ===")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2:   {r2:.3f}")

    # Compare against baseline formula on the test set
    baseline_preds = df.loc[X_test.index].apply(
        lambda row: calculate_clearance_time(
            row["num_vehicles"], row["avg_speed"], row["road_length"],
            row["signal_time"], row["arrival_rate"]
        ), axis=1
    )
    baseline_mae = mean_absolute_error(y_test, baseline_preds)
    print(f"\n=== Baseline Formula MAE ===\n{baseline_mae:.2f}")
    print(f"\nImprovement over baseline: {baseline_mae - mae:.2f} seconds lower MAE")

    # Feature importance
    importances = pd.Series(model.feature_importances_, index=FEATURE_COLUMNS)
    print("\n=== Feature Importance ===")
    print(importances.sort_values(ascending=False))

    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

    return model


if __name__ == "__main__":
    train_and_evaluate()
