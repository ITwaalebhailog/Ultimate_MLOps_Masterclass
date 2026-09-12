import sagemaker
from sagemaker.sklearn.model import SKLearnModel
from sagemaker import Session

sess = Session()
role = role = sagemaker.get_execution_role()
model_data = "s3://main-sagemaker-ml-healthcare/mlops/output/pipelines-6r22hriq6kjz-TrainModel-iiXe3tB7vb/output/model.tar.gz"   # existing tar.gz
entry_point = "inference.py"                       # local file

sk_model = SKLearnModel(
    model_data=model_data,
    role=role,
    entry_point=entry_point,
    framework_version="1.2-1",
    py_version="py3",
    sagemaker_session=sess
)

endpoint_name = "diabetes-endpoint-custom"
predictor = sk_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",   # or smaller if quota issues
    endpoint_name=endpoint_name
)

print("Deployed endpoint:", predictor.endpoint_name)