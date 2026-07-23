"""
predict.py
-----------
Loads the trained ML model and predicts clearance time
for new traffic input.
"""

import os
import sys
import joblib
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "preprocessing"))
from feature_engineering import add_features, encode_traffic_level

sys.path.append(os.path.dirname(__file__))
from baseline_math_model import get_traffic_level

MODEL_PATH = os.path.join(os.path.dirname(__file__), "traffic_model.pkl")

FEATURE_COLUMNS = [
    "num_vehicles", "avg_speed", "road_length", "signal_time",
    "arrival_rate", "flow_rate", "density", "speed_m_s", "traffic_level_encoded"
]


def load_model(path=MODEL_PATH):
    return joblib.load(path)


def predict_clearance_time(num_vehicles, avg_speed, road_length,
                            signal_time, arrival_rate, model=None):
    if model is None:
        model = load_model()

    traffic_level = get_traffic_level(num_vehicles)

    input_df = pd.DataFrame([{
        "num_vehicles": num_vehicles,
        "avg_speed": avg_speed,
        "road_length": road_length,
        "signal_time": signal_time,
        "arrival_rate": arrival_rate,
        "traffic_level": traffic_level
    }])

    input_df = add_features(input_df)
    input_df = encode_traffic_level(input_df)

    prediction = model.predict(input_df[FEATURE_COLUMNS])[0]

    return {
        "traffic_level": traffic_level,
        "num_vehicles": num_vehicles,
        "predicted_clearance_time": round(prediction, 2)
    }


if __name__ == "__main__":
    result = predict_clearance_time(
        num_vehicles=50,
        avg_speed=35.0,
        road_length=200.0,
        signal_time=45,
        arrival_rate=1.2
    )
    print(result)
