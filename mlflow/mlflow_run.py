import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline
import mlflow
import mlflow.sklearn
import os
from datetime import datetime

# ------------------ CONFIG ------------------
DATA_PATH = "./Datasets/diabetes.csv"   # path to your dataset (download from Kaggle)
EXPERIMENT_NAME = "mlflow-test"
MODEL_NAME = "mlops-diabetes-1"
RUN_PREFIX = "mlflow-run-test"
os.makedirs("./Datasets", exist_ok=True)
# --------------------------------------------

def preprocess_data(path):
    """Read CSV, replace zero values with medians, split into train/test."""
    df = pd.read_csv(path)
    
    # Replace 0 with NaN for these columns
    zero_as_missing = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    for col in zero_as_missing:
        df[col] = df[col].replace(0, np.nan)
        df[col].fillna(df[col].median(), inplace=True)
    
    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, n_estimators=100, max_depth=5):
    """Train RandomForestClassifier wrapped in a StandardScaler pipeline."""
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba)
    }
    return metrics

            


def main():
    # Load & preprocess
    X_train, X_test, y_train, y_test = preprocess_data(DATA_PATH)

    # Create experiment
    mlflow.set_experiment(EXPERIMENT_NAME)

    # Timestamp for unique run
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    run_name = f"{RUN_PREFIX}-{timestamp}"

    with mlflow.start_run(run_name=run_name) as run:
        # Log parameters
        n_estimators = 100
        max_depth = 5
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)

        # Train model
        model = train_model(X_train, y_train, n_estimators, max_depth)

        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test)
        for key, value in metrics.items():
            mlflow.log_metric(key, value)

        # Log model
        mlflow.sklearn.log_model(model, artifact_path="model")

        # Register model
        model_uri = f"runs:/{run.info.run_id}/model"
        mlflow.register_model(model_uri, MODEL_NAME)

        print(f"\n✅ Run completed: {run.info.run_id}")
        print(f"📊 Metrics: {metrics}")
        print(f"🔖 Registered model: {MODEL_NAME}")
        print("View the experiment in MLflow UI at http://127.0.0.1:5000")

if __name__ == "__main__":
    main()