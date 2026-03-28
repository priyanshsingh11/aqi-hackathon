# 🌬️ AQI Prediction Model — Ultimate Ensemble Approach
### Winning Hackathon Submission (Macro F1-Micro: 0.7948)

## 📌 Project Overview
The **AQI Prediction Project** was designed to tackle the complex, non-linear patterns of air pollution across various Indian cities and monitoring stations. Treating air quality not merely as static data but as a **dynamic time-series**, our solution utilizes advanced feature engineering and an ensemble of high-performance tree-based models to deliver industry-leading accuracy.

## 🗂️ Submission Package Structure Overview
- **`exploration.ipynb`**: Comprehensive Exploratory Data Analysis (EDA) uncovering seasonal spikes, station variance, and pandemic-era lockdown impacts.
- **`modeling.ipynb`**: Full model development lifecycle, including feature extraction, cross-validation, and ensemble strategy.
- **`inference.py`**: Production-ready standalone script that can process any CSV dataset for end-to-end predictions.
- **`best_model.pkl`**: The saved Binary of our "Ultimate Ensemble" (Random Forest + XGBoost + LightGBM).
- **`test_output.csv`**: Our final submission predictions for the 2,993 test records.
- **`report.docx`**: A detailed technical report outlining the project’s strategic intelligence.
- **`requirements.txt`**: Complete list of Python dependencies for model reproducibility.

---

## 🚀 Key Strategy: Why This Model Wins

### 1. Advanced Feature Engineering (The "Memory" Factor)
While raw PM2.5 and NO2 data are useful, they lack historical context. Our 23-feature set includes:
- **Rolling Statistics**: 3-day and 7-day smoothing to capture persistent trends.
- **Lags**: Capturing the "yesterday's air" correlation (90%+).
- **Cyclical Encoding**: Using `sin`/`cos` transforms for months and days to prevent the model from treating December and January as "far apart."
- **Station-Mean Proxy**: Calculating a historical "pollution floor" for each specific monitoring station.

### 2. The "Ultimate Ensemble"
We didn't rely on one model. Our **Soft Voting Classifier** combines the strengths of three leaders:
- **Random Forest**: Handles the baseline and prevents overfitting on outliers.
- **XGBoost**: Captures fine-grained interactions between pollutants.
- **LightGBM**: Implements histogram-based learning for rapid, highly-accurate convergence.

### 3. Exploitive EDA Insights
Our model is built on deep domain knowledge discovered in `exploration.ipynb`:
- **Winter Spikes**: Explicit handling of the stubble-burning and temperature-inversion spikes from October to January.
- **The Lockdown Factor**: Modeling the 2020 transition where industrial pollution dropped while domestic-source spikes remained.

---

## 🛠️ How to Run the Inference Script
To generate predictions from a new dataset:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python inference.py --input your_data.csv --output final_predictions.csv
   ```

---

## 📊 Final Performance Metrics
- **CV F1-Micro Score**: **0.7948 ± 0.0051**
- **Test Set Accuracy**: ~0.79
- **Top Feature Importance**: `PM2.5`, `PM2.5_lag_1`, `PM2.5_rolling_7`.

**Author:** [Your Name]
**Competition:** AQI Prediction Hackathon
