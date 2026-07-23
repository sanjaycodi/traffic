"""
main.py
--------
Entry point for the Traffic Clearance Time Prediction pipeline.

Run order:
    1. Ensures traffic.db is set up
    2. Loads clearance_train.csv -> DB (if not already loaded)
    3. Trains the ML model (if not already trained)
    4. Asks the user for traffic details, predicts, and saves the record to the DB
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "Database"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Conversion"))
sys.path.append(os.path.join(os.path.dirname(__file__), "models"))
sys.path.append(os.path.join(os.path.dirname(__file__), "crud"))

from SQL import create_table
from csv_to_db import load_csv_to_db
from train_model import train_and_evaluate, MODEL_PATH
from predict import predict_clearance_time, load_model
from baseline_math_model import calculate_clearance_time
from create import add_record


def get_user_input():
    """Prompt the user in the console for traffic details."""
    print("\nPlease enter the following details:")

    num_vehicles = int(input("Number of vehicles: "))
    avg_speed = float(input("Average vehicle speed (km/h): "))
    road_length = float(input("Road length / distance (m): "))
    signal_time = int(input("Signal time (seconds): "))
    arrival_rate = float(input("Vehicle arrival rate (vehicles/sec): "))

    return {
        "num_vehicles": num_vehicles,
        "avg_speed": avg_speed,
        "road_length": road_length,
        "signal_time": signal_time,
        "arrival_rate": arrival_rate
    }


def run_pipeline():
    print("Step 1: Setting up database...")
    create_table()

    print("\nStep 2: Loading CSV data into database...")
    load_csv_to_db()

    print("\nStep 3: Training ML model...")
    if not os.path.exists(MODEL_PATH):
        train_and_evaluate()
    else:
        print("Model already exists, skipping training. Delete traffic_model.pkl to retrain.")

    print("\nStep 4: Enter traffic details for prediction")
    model = load_model()

    user_input = get_user_input()

    ml_result = predict_clearance_time(**user_input, model=model)
    baseline_result = calculate_clearance_time(**user_input)

    print("\n================ FINAL OUTPUT ================")
    print(f"🚦 Traffic Level: {ml_result['traffic_level']}")
    print(f"🚗 Vehicles: {ml_result['num_vehicles']}")
    print(f"⏱️  Predicted Clearance Time (ML): {ml_result['predicted_clearance_time']} seconds")
    print(f"📐 Baseline Formula Estimate:     {baseline_result} seconds")
    print("================================================")

    # Save this entry (user input + prediction) into the database
    add_record(
        num_vehicles=user_input["num_vehicles"],
        avg_speed=user_input["avg_speed"],
        road_length=user_input["road_length"],
        signal_time=user_input["signal_time"],
        arrival_rate=user_input["arrival_rate"],
        traffic_level=ml_result["traffic_level"],
        clearance_time=ml_result["predicted_clearance_time"]
    )
    print("✅ This record has been saved to traffic.db")


if __name__ == "__main__":
    run_pipeline()