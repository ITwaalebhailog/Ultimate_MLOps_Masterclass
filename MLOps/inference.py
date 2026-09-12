# inference.py
import os
import joblib
import numpy as np

def model_fn(model_dir):
    # load model saved under /opt/ml/model/ inside container
    model_path = os.path.join(model_dir, "model.pkl")
    if not os.path.exists(model_path):
        # try other common name
        alt = os.path.join(model_dir, "model.joblib")
        if os.path.exists(alt):
            model_path = alt
        else:
            raise FileNotFoundError(f"Model file not found in {model_dir}: tried model.pkl and model.joblib")
    model = joblib.load(model_path)
    return model

def input_fn(request_body, content_type="text/csv"):
    if content_type == "text/csv":
        # single-row CSV string => numpy array shape (1, n_features)
        # allow newlines or trailing spaces
        s = request_body.strip()
        s = s.replace("\n", "")
        arr = np.fromstring(s, sep=",", dtype=float)
        return arr.reshape(1, -1)
    else:
        raise ValueError("Unsupported content type: " + content_type)

def predict_fn(input_data, model):
    return model.predict(input_data)

def output_fn(prediction, content_type="text/csv"):
    # return as simple CSV (or JSON if you prefer)
    return ",".join(map(str, prediction.tolist()))
