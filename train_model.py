"""
train_model.py
----------------
Trains the Random Forest model (the best performer from the notebook) and
saves it to disk so the web app can load it without retraining every time.

Tree depth and leaf size are capped on purpose: with ~1M rows, fully-grown
trees produced a ~2 GB model file (too large to deploy). Capping depth
shrinks the file to ~30 MB while barely moving accuracy (R^2 0.9999 -> 0.9991
on this dataset).

Run this ONCE (or whenever you get fresh data):
    python train_model.py

Requires: temperature_data.csv in the same folder.
NOTE: on ~1M rows with a single CPU core this can take 3-5 minutes.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

FEATURES = [
    'ambient', 'coolant', 'u_d', 'u_q', 'torque', 'i_d', 'i_q', 'pm',
    'stator_yoke', 'stator_tooth', 'stator_winding', 'profile_id'
]
TARGET = 'motor_speed'
MODEL_PATH = 'model.joblib'


def main():
    print("Loading data...")
    data = pd.read_csv('temperature_data.csv')

    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(
        n_estimators=20,
        max_depth=14,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Test MSE: {mse:.6f}")
    print(f"Test R2:  {r2:.6f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH} -- ready for the app.")


if __name__ == '__main__':
    main()
