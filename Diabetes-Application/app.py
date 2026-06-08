from flask import Flask, render_template, request, Response, g
import joblib
import numpy as np
import os
import csv
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

MODEL_PATH = "models/model.pkl"
SCALER_PATH = "models/scaler.pkl"
PREDICTIONS_LOG = "monitoring/predictions.csv"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]

os.makedirs("monitoring", exist_ok=True)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "flask_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"]
)
PREDICTION_COUNT = Counter(
    "ml_predictions_total",
    "Total model predictions",
    ["prediction"]
)
PREDICTION_PROB = Histogram(
    "ml_prediction_probability",
    "Prediction probability distribution",
    buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
)
INFERENCE_ERRORS = Counter(
    "ml_inference_errors_total",
    "Total inference errors"
)
LAST_PREDICTION_TS = Gauge(
    "ml_last_prediction_timestamp",
    "Last prediction timestamp"
)


def log_prediction(row: dict):
    file_exists = os.path.exists(PREDICTIONS_LOG)
    with open(PREDICTIONS_LOG, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


@app.before_request
def start_timer():
    g.start_time = time.time()


@app.after_request
def record_metrics(response):
    try:
        latency = time.time() - g.start_time
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
    except Exception:
        pass
    return response


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    prob = None

    if request.method == "POST":
        try:
            vals = [float(request.form.get(f, 0)) for f in FEATURES]
            arr = np.array(vals).reshape(1, -1)
            arr_scaled = scaler.transform(arr)

            pred = int(model.predict(arr_scaled)[0])
            prob = float(model.predict_proba(arr_scaled)[0, 1])

            result = "Diabetic" if pred == 1 else "Not Diabetic"

            PREDICTION_COUNT.labels(prediction=result).inc()
            PREDICTION_PROB.observe(prob)
            LAST_PREDICTION_TS.set(time.time())

            log_prediction({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                **{f: vals[i] for i, f in enumerate(FEATURES)},
                "prediction": pred,
                "probability": prob
            })

        except Exception as e:
            INFERENCE_ERRORS.inc()
            result = f"Error: {e}"

    return render_template("index.html", features=FEATURES, result=result, prob=prob)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)