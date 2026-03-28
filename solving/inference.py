import pandas as pd
import numpy as np
import joblib, argparse, os
import warnings
warnings.filterwarnings('ignore')

# -------------------------------------------------------------------------
# 1. THE BRAIN: Feature Engineering (MUST MATCH NOTEBOOK)
# -------------------------------------------------------------------------
def engineer_features(df):
    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 1. Temporal & Cyclical Features
    df["month"] = df["Date"].dt.month
    df["day_of_week"] = df["Date"].dt.dayofweek
    df["year"] = df["Date"].dt.year
    df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)
    df["month_sin"] = np.sin(2 * np.pi * df["month"]/12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"]/12)

    # 2. Season (Specialized India AQI)
    def get_season(m):
        if m in [11, 12, 1, 2]: return 1
        if m in [3, 4, 5, 6]: return 2
        return 3
    df["season"] = df["month"].apply(get_season)

    # 3. Rolling / Lag / Velocity (Grouped by Station)
    df = df.sort_values(["StationId", "Date"])
    for col in ["PM2.5", "NO2"]:
        df[f"{col}_rolling_3"] = df.groupby("StationId")[col].transform(lambda x: x.rolling(3, min_periods=1).mean())
        df[f"{col}_rolling_7"] = df.groupby("StationId")[col].transform(lambda x: x.rolling(7, min_periods=1).mean())
        df[f"{col}_std_7"] = df.groupby("StationId")[col].transform(lambda x: x.rolling(7, min_periods=1).std()).fillna(0)
        df[f"{col}_lag_1"] = df.groupby("StationId")[col].shift(1).fillna(method="bfill")
        df[f"{col}_diff_1"] = df[col] - df[f"{col}_lag_1"]

    # 4. Ratio and Station historical Proxy
    df["PM_NO2_ratio"] = df["PM2.5"] / (df["NO2"] + 1e-5)
    
    # Map from the current data (proxy for the test set)
    df['Station_Mean_PM2.5'] = df.groupby('StationId')['PM2.5'].transform('mean').fillna(df['PM2.5'].mean())

    return df

# -------------------------------------------------------------------------
# 2. RUNTIME: Load Model and Predict
# -------------------------------------------------------------------------
def run_inference(input_path, output_path):
    # Load winning ensemble artifacts
    if not all(os.path.exists(f) for f in ["best_model.pkl", "le_target.pkl", "le_city.pkl", "le_station.pkl"]):
        raise FileNotFoundError("Missing model or encoder .pkl files in current directory.")
        
    model = joblib.load("best_model.pkl")
    le_target = joblib.load("le_target.pkl")
    le_city = joblib.load("le_city.pkl")
    le_station = joblib.load("le_station.pkl")
    
    # Load and process data
    raw_df = pd.read_csv(input_path)
    df = raw_df.copy()
    
    # Apply Advanced Features
    df = engineer_features(df)
    
    # Encodings
    df["City_Enc"] = le_city.transform(df["City"])
    df["Station_Enc"] = le_station.transform(df["StationId"])
    
    # FEATURE_COLS: Must align 100% with the notebook order
    FEATURE_COLS = [
        "PM2.5", "NO2", "month", "day_of_week", "year", "season", "is_weekend",
        "month_sin", "month_cos",
        "PM2.5_rolling_3", "PM2.5_rolling_7", "NO2_rolling_3", "NO2_rolling_7",
        "PM2.5_std_7", "NO2_std_7",
        "PM2.5_lag_1", "NO2_lag_1", 
        "PM2.5_diff_1", "NO2_diff_1",
        "PM_NO2_ratio", "Station_Mean_PM2.5",
        "City_Enc", "Station_Enc"
    ]
    
    # Predict using the Ensemble
    X_val = df[FEATURE_COLS].astype(float).values
    preds = model.predict(X_val)
    preds_labels = le_target.inverse_transform(preds)
    
    # Map predictions back to the original row order
    df["AQI_Bucket"] = preds_labels
    final_output = raw_df[["City", "StationId", "Date"]].merge(
        df[["City", "StationId", "Date", "AQI_Bucket"]], 
        on=["City", "StationId", "Date"], 
        how="left"
    )
    
    final_output.to_csv(output_path, index=False)
    print(f"DONE! Final predictions saved as: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    try:
        run_inference(args.input, args.output)
    except Exception as e:
        print(f"ERROR: {e}")
