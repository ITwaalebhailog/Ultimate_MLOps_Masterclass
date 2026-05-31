######################  imports  ###################################
from sagemaker import Session
import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.pipeline_context import PipelineSession
import boto3
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.estimator import SKLearn
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sagemaker.sklearn import SKLearn
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep
from sagemaker.workflow.model_step import ModelStep
from sagemaker.sklearn.model import SKLearnModel
from sagemaker.workflow.parameters import ParameterInteger, ParameterString
from sagemaker.workflow.steps import ProcessingStep, CreateModelStep
from sagemaker.workflow.conditions import ConditionGreaterThan
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.functions import JsonGet
from sagemaker.model import Model
from sagemaker.inputs import CreateModelInput
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.workflow.model_step import ModelStep


###################  parameters #####################
bucket='main-sagemaker-ml-healthcare'
prefix = 'mlops'
input_source = f"s3://{bucket}/{prefix}/diabetes.csv"
train_path = f"s3://{bucket}/{prefix}/train"
test_path = f"s3://{bucket}/{prefix}/test"
val_path = f"s3://{bucket}/{prefix}/val"
model_output_uri = "s3://{}/{}/output".format(bucket, prefix)
train_data_uri = train_path
test_data_uri = test_path
train_input = TrainingInput(s3_data=train_data_uri, content_type='text/csv')
evaluation_output_uri = f"s3://{bucket}/output/evaluation"

################# important for pipeline #####################
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()
pipeline_session = PipelineSession()
########### preprocessing of data ##################

sklearn_processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=role,
    instance_type="ml.m5.large",
    instance_count=1, 
    base_job_name='diabetes-main'
)

# Define processing step
processing_step = ProcessingStep(
    name='PreprocessingStep',
    processor=sklearn_processor,
    code='preprocess.py',  # Path to your preprocessing script
    inputs=[
        ProcessingInput(
            source=input_source, 
            destination="/opt/ml/processing/input",
            s3_input_mode="File",
            s3_data_distribution_type="ShardedByS3Key",
            
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name="train_data", 
            source="/opt/ml/processing/output/train",
            destination=train_path,
            s3_upload_mode="EndOfJob",
        ),
        ProcessingOutput(
            output_name="test_data", 
            source="/opt/ml/processing/output/test",
            destination=test_path,
            s3_upload_mode="EndOfJob",
        ),
        ProcessingOutput(
            output_name="val_data", 
            source="/opt/ml/processing/output/validation",
            destination=val_path,
            s3_upload_mode="EndOfJob",
        ),
    ]
)

########  train step ###########

estimator = SKLearn(entry_point='train.py',
                    framework_version="1.2-1",
                    py_version='py3',
                    instance_type='ml.m5.xlarge',
                    role=role,
                    output_path=model_output_uri,
                    base_job_name='sklearn-iris',
                    hyperparameters={'n_estimators': 50, 'max_depth': 5})
# Define the input data for training and testing
train_step = TrainingStep(
    name="TrainModel",
    estimator=estimator,
    inputs={
        "training": train_input,
    },
)

####### eval and register model and check the condition ######
image_uri = sagemaker.image_uris.retrieve(
        framework="sklearn",
        region=region,
        version=sklearn_version,
        py_version=py_version
    )

##### train artifacts ######
model_artifact_path = train_step.properties.ModelArtifacts.S3ModelArtifacts
########
evaluation_report = PropertyFile(
    name="EvaluationReport",
    output_name="evaluation",
    path="evaluation.json"
)

# Initialize the ScriptProcessor
evaluation_processor = ScriptProcessor(
    image_uri=image_uri,
    command=["python3"],
    instance_type="ml.m5.large",
    instance_count=1,
    role=role,  # Replace with your actual role ARN
    sagemaker_session=pipeline_session
)

# Define the processing step for evaluation
evaluation_step = ProcessingStep(
    name="EvaluateModel",
    processor=evaluation_processor,
    inputs=[
        ProcessingInput(source=model_artifact_path, destination="/opt/ml/processing/model"),
        ProcessingInput(source=test_path, destination="/opt/ml/processing/test"),
    ],
    outputs=[
        ProcessingOutput(output_name="evaluation", source="/opt/ml/processing/output", destination=evaluation_output_uri),
    ],
    code="eval.py",
    property_files=[evaluation_report]
)

# Define ModelMetrics for registration (optional, to track accuracy and other metrics)
model_metrics = ModelMetrics(
    model_statistics=MetricsSource(
        s3_uri=f"{evaluation_output_uri}/evaluation.json",
        content_type="application/json"
    )
)

# Create a model registration step with the diabetes model registry
model = Model(
    image_uri=image_uri,
    model_data=model_artifact_path,
    role=role,  # Replace with your actual role ARN
    sagemaker_session=pipeline_session  # Attach the pipeline session here
)

register_args = model.register(
    content_types=["application/x-model"],
    response_types=["application/json"],
    inference_instances=["ml.m5.large"],
    transform_instances=["ml.m5.large"],
    model_package_group_name="diabetes",  # Specify the model group name here
    model_metrics=model_metrics  # Optional: Attach model metrics
)
step_register = ModelStep(name="diabetes", step_args=register_args)


# Define the condition to check accuracy
cond_gte = ConditionGreaterThan(
    left=JsonGet(
        step_name=evaluation_step.name,
        property_file=evaluation_report,
        json_path="accuracy"
    ),
    right=0.60
)

# Create a condition step
condition_step = ConditionStep(
    name="CheckAccuracy",
    conditions=[cond_gte],
    if_steps=[step_register],  # Register the model if accuracy > 60%
    else_steps=[]  # Do nothing if the accuracy is <= 60%
)

train_step.add_depends_on([processing_step])
evaluation_step.add_depends_on([train_step])
condition_step.add_depends_on([evaluation_step])

# Define the pipeline
pipeline = Pipeline(
    name="model-evaluation-pipeline-master-3",
    steps=[processing_step, train_step, evaluation_step, condition_step],
    sagemaker_session=pipeline_session,  # Ensure the session is passed here
)

# Create and start the pipeline using SageMaker client
pipeline.create(role_arn=role)  # Replace with your actual role ARN
pipeline.start()
