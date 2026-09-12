import boto3

client = boto3.client("sagemaker-runtime", region_name="ap-south-1")

payload = "6,148,72,33.6,0.627,50"

res = client.invoke_endpoint(
    EndpointName="diabetes-endpoint-custom",
    Body=payload,
    ContentType="text/csv",
    Accept="text/csv"
)

print(res['Body'].read().decode())