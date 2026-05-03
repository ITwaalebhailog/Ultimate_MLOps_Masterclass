# app.py
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

MODEL_PATH = "models/model.pkl"
SCALER_PATH = "models/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

FEATURES = ["Pregnancies","Glucose","BloodPressure","BMI","DiabetesPedigreeFunction","Age"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    prob = None
    if request.method == "POST":
        # Read inputs from form (string -> float)
        try:
            vals = [float(request.form.get(f, 0)) for f in FEATURES]
            arr = np.array(vals).reshape(1, -1)
            arr_scaled = scaler.transform(arr)
            pred = model.predict(arr_scaled)[0]
            prob = model.predict_proba(arr_scaled)[0,1]
            result = "Diabetic" if pred == 1 else "Not Diabetic"
        except Exception as e:
            result = f"Error: {e}"
    return render_template("index.html", features=FEATURES, result=result, prob=prob)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)