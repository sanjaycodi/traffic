@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Generating synthetic dataset (if not present)...
if not exist clearance_train.csv (
    python generate_synthetic_data.py
)

echo Running Traffic Clearance Prediction pipeline...
python traffic\main.py

pause
