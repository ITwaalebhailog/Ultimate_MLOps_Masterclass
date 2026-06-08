import os
import pandas as pd
from evidently.report import Report
from evidently.presets import DataDriftPreset

REFERENCE_PATH = "data/reference.csv"
CURRENT_PATH = "monitoring/predictions.csv"
OUTPUT_DIR = "monitoring/reports"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "drift_report.html")

os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(REFERENCE_PATH):
    raise FileNotFoundError(f"Reference dataset not found: {REFERENCE_PATH}")

if not os.path.exists(CURRENT_PATH):
    raise FileNotFoundError(f"Current prediction log not found: {CURRENT_PATH}")

reference_df = pd.read_csv(REFERENCE_PATH)
current_df = pd.read_csv(CURRENT_PATH)

# Use only the feature columns for input drift
feature_cols = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]

reference_df = reference_df[feature_cols]
current_df = current_df[feature_cols]

report = Report([DataDriftPreset()])
report.run(reference_data=reference_df, current_data=current_df)
report.save_html(OUTPUT_PATH)

print(f"Drift report saved to {OUTPUT_PATH}")