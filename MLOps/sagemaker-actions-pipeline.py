######################################################
#                     IMPORTS                         #
######################################################
import os
import sys
import json
import datetime
import time               # added
import boto3              # added
import sagemaker
from sagemaker import get_execution_role
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CacheConfig
from sagemaker.processing import ProcessingInput, ProcessingOutput, ScriptProcessor
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.functions import JsonGet
from sagemaker.workflow.conditions import ConditionGreaterThan
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.model import Model
from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.workflow.model_step import ModelStep

######################################################
#               READ PARAMETERS FROM JSON            #
######################################################
def read_pipeline_params():
    """Load pipeline configuration from parameters.json"""
    params_path = os.path.join(os.path.dirname(__file__), "parameters.json")
    with open(params_path, "r") as f:
        return json.load(f)

######################################################
#                MAIN PIPELINE FUNCTION              #
######################################################
def get_pipeline() -> str:
    # ---------- Load parameters ----------
    params = read_pipeline_params()

    bucket = params["bucket"]
    prefix = params["prefix"]
    region = params.get("region", "ap-south-1")
    role = params.get("role", sagemaker.get_execution_role())  # fallback to default role

    # Instance types
    preprocessing_instance = params["preprocessing_instance_type"]
    training_instance = params["training_instance_type"]
    evaluation_instance = params["evaluation_instance_type"]
    instance_count = params["instance_count"]

    # Model package group
    model_package_group = params["model_package_group_name"]

    # Framework versions
    sklearn_version = params["framework_version_sklearn"]
    xgboost_version = params["framework_version_xgboost"]
    py_version = params["py_version"]

    # Hyperparameters
    hyperparameters = params["hyperparameters"]

    # ---------- Git / PR info from command line ----------
    # Expected: python pipeline.py <branch> <pr_number> <pr_status>
    current_branch = sys.argv[1] if len(sys.argv) > 1 else "local"
    pr_number = sys.argv[2] if len(sys.argv) > 2 else ""
    pr_status = sys.argv[3] if len(sys.argv) > 3 else ""

    # ---------- Sessions & cache ----------
    sagemaker_session = sagemaker.Session()
    pipeline_session = PipelineSession()
    cache_config = CacheConfig(enable_caching=True, expire_after="T30m")  # 30 minutes

    # ---------- Unique timestamp for this run ----------
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    run_output_path = f"s3://{bucket}/{prefix}/pipeline_runs/{timestamp}"

    # ---------- Pipeline parameters (for EventBridge triggers) ----------
    input_data_param = ParameterString(
        name="InputDataUri",
        default_value=params["input_data_default"]   # will be overridden by EventBridge
    )

    # ---------- Step 1 : Preprocessing ----------
    sklearn_processor = SKLearnProcessor(
        framework_version=sklearn_version,
        role=role,
        instance_type=preprocessing_instance,
        instance_count=instance_count,
        base_job_name=f"{prefix}-preprocess",
        sagemaker_session=pipeline_session
    )

    processing_step = ProcessingStep(
        name="Preprocessing",
        processor=sklearn_processor,
        code="MLOps/preprocess.py",   # your preprocessing script
        inputs=[
            ProcessingInput(
                source=input_data_param,
                destination="/opt/ml/processing/input",
                s3_input_mode="File",
                s3_data_distribution_type="ShardedByS3Key"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="train",
                source="/opt/ml/processing/output/train",
                destination=f"{run_output_path}/train",
                s3_upload_mode="EndOfJob"
            ),
            ProcessingOutput(
                output_name="test",
                source="/opt/ml/processing/output/test",
                destination=f"{run_output_path}/test",
                s3_upload_mode="EndOfJob"
            ),
            ProcessingOutput(
                output_name="validation",
                source="/opt/ml/processing/output/validation",
                destination=f"{run_output_path}/validation",
                s3_upload_mode="EndOfJob"
            )
        ],
        cache_config=cache_config
    )

    # ---------- Step 2 : Training ----------
    estimator = SKLearn(
        entry_point="MLOps/train.py",
        framework_version=sklearn_version,
        py_version=py_version,
        instance_type=training_instance,
        role=role,
        output_path=f"{run_output_path}/model",
        base_job_name=f"{prefix}-train",
        hyperparameters=hyperparameters,
        sagemaker_session=pipeline_session
    )

    train_step = TrainingStep(
        name="Training",
        estimator=estimator,
        inputs={
            "training": TrainingInput(
                s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
                content_type="text/csv"
            )
        },
        cache_config=cache_config
    )

    # ---------- Step 3 : Evaluation ----------
    image_uri = sagemaker.image_uris.retrieve(
        framework="sklearn",
        region=region,
        version=sklearn_version,
        py_version=py_version
    )

    evaluation_processor = ScriptProcessor(
        image_uri=image_uri,
        command=["python3"],
        instance_type=evaluation_instance,
        instance_count=instance_count,
        role=role,
        sagemaker_session=pipeline_session,
        base_job_name=f"{prefix}-evaluate"
    )

    evaluation_report = PropertyFile(
        name="EvaluationReport",
        output_name="evaluation",
        path="evaluation.json"
    )

    evaluation_step = ProcessingStep(
        name="Evaluation",
        processor=evaluation_processor,
        code="MLOps/eval.py",   # your evaluation script
        inputs=[
            ProcessingInput(
                source=train_step.properties.ModelArtifacts.S3ModelArtifacts,
                destination="/opt/ml/processing/model"
            ),
            ProcessingInput(
                source=processing_step.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
                destination="/opt/ml/processing/test"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="evaluation",
                source="/opt/ml/processing/output",
                destination=f"{run_output_path}/evaluation"
            )
        ],
        property_files=[evaluation_report],
        cache_config=cache_config
    )

    # ---------- Step 4 : Condition & Model Registration ----------
    model = Model(
        image_uri=image_uri,
        model_data=train_step.properties.ModelArtifacts.S3ModelArtifacts,
        role=role,
        sagemaker_session=pipeline_session
    )

    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri=f"{run_output_path}/evaluation/evaluation.json",
            content_type="application/json"
        )
    )

    register_args = model.register(
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.m5.large"],
        transform_instances=["ml.m5.large"],
        model_package_group_name=model_package_group,
        model_metrics=model_metrics,
        approval_status="PendingManualApproval"
    )
    register_step = ModelStep(name="RegisterModel", step_args=register_args)

    # Condition: accuracy > 0.60
    condition = ConditionGreaterThan(
        left=JsonGet(
            step_name=evaluation_step.name,
            property_file=evaluation_report,
            json_path="accuracy"
        ),
        right=0.60
    )

    condition_step = ConditionStep(
        name="CheckAccuracy",
        conditions=[condition],
        if_steps=[register_step],
        else_steps=[]
    )

    # ---------- Set dependencies ----------
    train_step.add_depends_on([processing_step])
    evaluation_step.add_depends_on([train_step])
    condition_step.add_depends_on([evaluation_step])

    # ---------- Conditional pipeline based on branch ----------
    # If on main branch, run everything; otherwise skip registration
    pipeline_name = params.get("pipeline_name", "model-evaluation-pipeline")

    if current_branch == "mlops" or (current_branch.startswith("feature-") and pr_status == "merged"):
        steps = [processing_step, train_step, evaluation_step, condition_step]
    else:
        # For feature branches / PRs, stop after evaluation (no registration)
        steps = [processing_step, train_step, evaluation_step]

    pipeline = Pipeline(
        name=pipeline_name,
        parameters=[input_data_param],
        steps=steps,
        sagemaker_session=pipeline_session
    )

    # ---------- Upsert and start ----------
    pipeline.upsert(role_arn=role)
    execution = pipeline.start()

    # ========== NEW: WAIT FOR COMPLETION ==========
    sagemaker_client = boto3.client('sagemaker')
    exec_arn = execution.arn

    print(f"Pipeline execution started: {exec_arn}")
    print("Waiting for execution to finish...")

    while True:
        response = sagemaker_client.describe_pipeline_execution(
            PipelineExecutionArn=exec_arn
        )
        status = response['PipelineExecutionStatus']
        print(f"Current status: {status}")
        if status not in ['Executing', 'Stopping']:
            break
        time.sleep(30)

    # Final result handling
    if status == 'Succeeded':
        print("✅ Pipeline execution succeeded!")
        # Get the display name from the last describe response
        display_name = response.get('PipelineExecutionDisplayName', exec_arn.split('/')[-1])
        identifier = f"{run_output_path}^{timestamp}^{display_name}^{exec_arn}"
        print(identifier)
        return identifier
    else:
        print(f"❌ Pipeline execution failed with status: {status}")
        if 'FailureReason' in response:
            print(f"Reason: {response['FailureReason']}")
        sys.exit(1)   # make GitHub Actions job fail

if __name__ == "__main__":
    get_pipeline()