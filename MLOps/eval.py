import argparse
import os
import joblib
import pandas as pd
import tarfile
import json
from sklearn.metrics import accuracy_score, classification_report

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-data-dir', type=str, default='/opt/ml/processing/output')
    parser.add_argument('--model-dir', type=str, default='/opt/ml/processing/model')
    parser.add_argument('--test', type=str, default='/opt/ml/processing/test')
    return parser.parse_args()

def extract_model(model_dir):
    # Path to the model tar.gz file
    model_tar_path = os.path.join(model_dir, 'model.tar.gz')
    
    # Extract the tar.gz file
    with tarfile.open(model_tar_path, 'r:gz') as tar:
        tar.extractall(path=model_dir)
    
    # Return the path to the extracted model
    return os.path.join(model_dir, "model.joblib")

if __name__ == "__main__":
    args = _parse_args()

    # Extract and load the model
    model_path = extract_model(args.model_dir)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    model = joblib.load(model_path)

    # Load test data
    test_data = pd.read_csv(os.path.join(args.test, "diabetes_test.csv"))
    test_x = test_data.iloc[:, :-1]
    test_y = test_data.iloc[:, -1]

    # Make predictions
    predictions = model.predict(test_x)

    # Evaluate the model
    accuracy = accuracy_score(test_y, predictions)
    report = classification_report(test_y, predictions, output_dict=True)

    # Write out evaluation report
    evaluation_output_dir = args.output_data_dir
    os.makedirs(evaluation_output_dir, exist_ok=True)
    
    with open(os.path.join(evaluation_output_dir, "evaluation.json"), "w") as f:
        json.dump({"accuracy": accuracy, "classification_report": report}, f)

    print(f"Model accuracy: {accuracy:.4f}")

    # Write accuracy to a separate file for the pipeline condition
    with open(os.path.join(evaluation_output_dir, "accuracy.json"), "w") as f:
        json.dump({"accuracy": accuracy}, f)