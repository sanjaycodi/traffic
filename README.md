# 🚦 Traffic Clearance Time Prediction Using Machine Learning

Predicts how long it will take to clear traffic at a signalized junction,
using both a mathematical baseline model and a trained ML model (Random Forest).

## Project Structure

```
Traffic_Clearance_Prediction/
├── traffic/
│   ├── Conversion/
│   │   ├── csv_to_db.py
│   │   └── db_to_csv.py
│   ├── crud/
│   │   ├── create.py
│   │   ├── read.py
│   │   ├── update.py
│   │   └── delete.py
│   ├── Database/
│   │   ├── SQL.py
│   │   └── traffic.db
│   ├── models/
│   │   ├── baseline_math_model.py
│   │   ├── train_model.py
│   │   ├── predict.py
│   │   └── traffic_model.pkl
│   ├── preprocessing/
│   │   ├── feature_engineering.py
│   │   └── data_cleaning.py
│   └── main.py
├── generate_synthetic_data.py
├── clearance_train.csv
├── requirements.txt
├── run.bat
└── README.md
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Generate a synthetic dataset (skip if you have real data):
   ```
   python generate_synthetic_data.py
   ```

3. Run the full pipeline:
   ```
   python traffic/main.py
   ```

   Or on Windows, just double-click `run.bat`.

## How It Works

1. **Data** — `clearance_train.csv` is loaded into a SQLite database (`traffic.db`)
   via `Conversion/csv_to_db.py`.
2. **CRUD** — records can be added/viewed/updated/deleted via the `crud/` scripts.
3. **Preprocessing** — `preprocessing/feature_engineering.py` computes flow rate,
   density, and speed in m/s; `data_cleaning.py` removes invalid/missing rows.
4. **Baseline Model** — `models/baseline_math_model.py` computes an estimated
   clearance time using a traffic-flow formula (no ML).
5. **ML Model** — `models/train_model.py` trains a Random Forest Regressor and
   compares its accuracy (MAE/RMSE) against the baseline formula.
6. **Prediction** — `models/predict.py` loads the trained model and predicts
   clearance time for new input.
7. **main.py** ties all steps together and prints the final result:
   ```
   🚦 Traffic Level: High
   🚗 Vehicles: 50
   ⏱️  Predicted Clearance Time (ML): 120.45 seconds
   📐 Baseline Formula Estimate:     118.6 seconds
   ```

## Retraining the Model

Delete `traffic/models/traffic_model.pkl` and re-run `main.py` to retrain
on updated data.




