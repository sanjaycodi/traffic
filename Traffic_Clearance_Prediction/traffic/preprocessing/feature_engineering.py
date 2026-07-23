"""
feature_engineering.py
-----------------------
Builds derived features (traffic flow, density) from raw traffic data.
"""

import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds:
        flow_rate       = num_vehicles / signal_time
        density         = num_vehicles / road_length
        speed_m_s       = avg_speed converted to m/s
    """
    df = df.copy()

    df["flow_rate"] = df["num_vehicles"] / df["signal_time"]
    df["density"] = df["num_vehicles"] / df["road_length"]
    df["speed_m_s"] = df["avg_speed"] * 1000 / 3600

    return df


def encode_traffic_level(df: pd.DataFrame) -> pd.DataFrame:
    """Encodes traffic_level (Low/Medium/High) into numeric form for ML models."""
    df = df.copy()
    mapping = {"Low": 0, "Medium": 1, "High": 2}
    df["traffic_level_encoded"] = df["traffic_level"].map(mapping)
    return df


if __name__ == "__main__":
    sample = pd.read_csv("../../clearance_train.csv")
    sample = add_features(sample)
    sample = encode_traffic_level(sample)
    print(sample.head())
