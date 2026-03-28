#!/usr/bin/env python3
"""
AQI Prediction — Inference Script
===================================
Usage:
    python inference.py --input test.csv --output predictions.csv
    python inference.py --input any_data.csv              # saves to output.csv by default

What you MUST fill in
----------------------
    1. engineer_features()  — same feature engineering you did in modeling.ipynb
    2. FEATURE_COLS         — same list and order you used when training
    3. MODEL_PATH           — path to your saved model file
"""

import argparse
import sys
import os
import pandas as pd
import numpy as np
import joblib


# ── Change this to your saved model filename ──────────────────────────────────
MODEL_PATH = 'best_model.pkl'

# ── Set this to exactly match your training feature list ──────────────────────
FEATURE_COLS = [
    # e.g. 'PM2.5', 'NO2', 'month', 'year', ...
]


# ── Fill this function with your feature engineering ──────────────────────────
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the same feature engineering used during training.

    - Input : raw dataframe (same columns as train.csv / test.csv, no label column)
    - Output: dataframe containing all columns listed in FEATURE_COLS

    Important: any aggregate computed from training data (e.g. per-city median PM2.5)
    must be hard-coded as a dictionary here since we have no training data at runtime.
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])

    # YOUR CODE — add your features here
    # Example (replace with your actual work):
    #   df['month']       = df['Date'].dt.month
    #   df['day_of_week'] = df['Date'].dt.dayofweek
    #   df['is_winter']   = df['month'].isin([11, 12, 1, 2]).astype(int)

    return df


# ── Core logic — no need to edit below this line ──────────────────────────────

def predict(input_path: str, output_path: str) -> None:
    #############################################################################################
    # NOTE:                                                                                     #
    # This is example function, you are free to write inference code as per your requirement    #
    #############################################################################################
    # Load model
    if not os.path.exists(MODEL_PATH):
        sys.exit(f"[ERROR] Model file not found: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    print(f"[OK] Model loaded       : {MODEL_PATH}")

    # Load input CSV
    if not os.path.exists(input_path):
        sys.exit(f"[ERROR] Input file not found: {input_path}")
    df = pd.read_csv(input_path)
    print(f"[OK] Input loaded       : {input_path}  ({len(df):,} rows)")

    # Check minimum required columns
    required = ['City', 'StationId', 'Date', 'PM2.5', 'NO2']
    missing  = [c for c in required if c not in df.columns]
    if missing:
        sys.exit(f"[ERROR] Input CSV is missing columns: {missing}")

    # Feature engineering
    if not FEATURE_COLS:
        sys.exit("[ERROR] FEATURE_COLS is empty — fill it in at the top of this script.")
    df_fe = engineer_features(df)

    missing_feat = [c for c in FEATURE_COLS if c not in df_fe.columns]
    if missing_feat:
        sys.exit(f"[ERROR] engineer_features() did not produce: {missing_feat}")

    X = df_fe[FEATURE_COLS].astype(float).values

    if np.isnan(X).any():
        sys.exit(f"[ERROR] {np.isnan(X).sum()} NaN value(s) in feature matrix — check engineer_features().")

    # Predict
    predictions = model.predict(X)
    print(f"[OK] Predictions done   : {len(predictions):,} rows")

    # Build output
    out = df[['City', 'StationId', 'Date']].copy()
    out['Date']       = pd.to_datetime(out['Date']).dt.strftime('%Y-%m-%d')
    out['AQI_Bucket'] = predictions

    out.to_csv(output_path, index=False)
    print(f"[OK] Output saved to    : {output_path}")
    print(f"\n     Prediction counts:")
    for label, count in out['AQI_Bucket'].value_counts().items():
        print(f"       {str(label):<15s} {count:5d}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AQI Prediction Inference Script')
    parser.add_argument('--input',  '-i', required=True,       help='Input CSV file path')
    parser.add_argument('--output', '-o', default='output.csv', help='Output CSV file path')
    args = parser.parse_args()
    predict(args.input, args.output)
