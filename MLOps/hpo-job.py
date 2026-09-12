import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.tuner import (
    HyperparameterTuner,
    IntegerParameter,
)

session = sagemaker.Session()
role = sagemaker.get_execution_role()

# SKLearn Estimator
estimator = SKLearn(
    entry_point="hyperparameter.py",
    role=role,
    instance_type="ml.m5.large",
    framework_version="1.2-1",
    hyperparameters={
        "min_samples_split": 2
    }
)

# Define hyperparameter ranges to tune
hyperparameter_ranges = {
    "n_estimators": IntegerParameter(50, 300),
    "max_depth": IntegerParameter(3, 15),
}

objective_metric_name = "Accuracy"
metric_definitions = [{"Name": "Accuracy", "Regex": "Accuracy: (.*)"}]

tuner = HyperparameterTuner(
    estimator,
    objective_metric_name,
    hyperparameter_ranges,
    metric_definitions,
    max_jobs=5,         # total training jobs
    max_parallel_jobs=2 # run these many jobs in parallel
)

# Launch HPO job
tuner.fit({"train": "s3://main-sagemaker-ml-healthcare/mlops/train/"})

print("Hyperparameter tuning job started.")
