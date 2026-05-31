# data_prep_and_train.py
import pandas as pd
#import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
import joblib
import os


# --- CONFIG ---
DATA_PATH = "Datasets/diabetes.csv"   # path to CSV
MODEL_OUT = "models/model.pkl"
SCALER_OUT = "models/scaler.pkl"
os.makedirs("models", exist_ok=True)

# --- LOAD ---
df = pd.read_csv(DATA_PATH)
print("Dataset shape:", df.shape)
print(df.head())

# --- QUICK EDA (optional) ---
print(df.describe())
df.drop(['SkinThickness','Insulin'], axis=1, inplace=True)
# --- CLEANING ---
# In this dataset, some features have 0 as placeholder for missing:
zero_as_missing = ["Glucose", "BloodPressure", "BMI"]
# Replace 0 with np.nan

for col in zero_as_missing:
    median_value = df[col].median()
    df[col] = df[col].replace(0, median_value)

# --- FEATURES / TARGET ---
X = df.drop("Outcome", axis=1)  # Outcome is 0/1 (no/yes)
y = df["Outcome"]

# --- TRAIN/TEST SPLIT ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Train/test shapes:", X_train.shape, X_test.shape)

# --- SCALE ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- MODEL: RandomForest ---
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)

# --- EVALUATE ---
y_pred = rf.predict(X_test_scaled)
y_proba = rf.predict_proba(X_test_scaled)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# --- OPTIONAL: Hyperparameter tuning (uncomment to run) ---
param_grid = {
     "n_estimators": [100, 200],
     "max_depth": [None, 5, 10],
     "min_samples_split": [2, 5],
     "min_samples_leaf": [1, 2],
} ##
gs = GridSearchCV(RandomForestClassifier(random_state=42), param_grid,
                   cv=5, scoring="roc_auc", n_jobs=-1, verbose=2)
gs.fit(X_train_scaled, y_train)
print("Best params:", gs.best_params_)
rf = gs.best_estimator_

# --- SAVE MODEL & SCALER ---
joblib.dump(rf, MODEL_OUT)
joblib.dump(scaler, SCALER_OUT)
print("Saved model to", MODEL_OUT)
print("Saved scaler to", SCALER_OUT)