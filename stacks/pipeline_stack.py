from aws_cdk import (
    aws_codepipeline as codepipeline,
    SecretValue,
    aws_iam as iam,
    aws_lambda as _lambda,
    Stack,
    Stage
)
from constructs import Construct
from aws_cdk.pipelines import ShellStep, CodePipelineSource, CodePipeline
import boto3

secret_client = boto3.client('secretsmanager')

response = secret_client.get_secret_value(
    SecretId='arn:aws:secretsmanager:ap-southeast-1:682853212408:secret:cdk-token'
)

class CdkSampleStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        

        # Define the pipeline
        pipeline = CodePipeline(self, "Pipeline",
            pipeline_name="AjuramPipeline",
            synth=ShellStep("Synth",
                input=CodePipelineSource.git_hub(
                    "Ajuram-Prasanna/CDK-Ajuram", "main",
                    authentication=SecretValue.unsafe_plain_text(response['SecretString'])
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "npx cdk synth"
                ]
            )
        )

