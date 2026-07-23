"""
data_cleaning.py
-----------------
Basic cleaning utilities: handle missing values, remove duplicates,
and filter invalid rows.
"""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Drop exact duplicate rows
    df = df.drop_duplicates()

    # Drop rows with missing critical values
    required_cols = ["num_vehicles", "avg_speed", "road_length",
                      "signal_time", "arrival_rate", "clearance_time"]
    df = df.dropna(subset=required_cols)

    # Remove invalid/negative values
    df = df[(df["num_vehicles"] > 0) &
            (df["avg_speed"] > 0) &
            (df["road_length"] > 0) &
            (df["signal_time"] > 0) &
            (df["clearance_time"] > 0)]

    return df.reset_index(drop=True)


if __name__ == "__main__":
    sample = pd.read_csv("../../clearance_train.csv")
    cleaned = clean_data(sample)
    print(f"Rows before cleaning: {len(sample)}, after cleaning: {len(cleaned)}")
