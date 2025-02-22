from aws_cdk import (
    SecretValue,
    Stack,
    aws_codebuild as codebuild,
    aws_logs as logs,
)
from constructs import Construct
from aws_cdk.pipelines import CodePipelineSource
import boto3

from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines as pipelines,
)

class CdkSampleStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.secret_client = boto3.client('secretsmanager')

        self.response = self.secret_client.get_secret_value(
            SecretId='arn:aws:secretsmanager:ap-southeast-1:682853212408:secret:cdk-token'
        )

        # Define the log group
        log_group = logs.LogGroup(self, "PipelineLogGroup")

        # Define the build project with logging
        build_project = codebuild.PipelineProject(self, "BuildProject",
            logging=codebuild.LoggingOptions(
                cloud_watch=codebuild.CloudWatchLoggingOptions(
                    enabled=True,
                    log_group=log_group,
                    prefix="build-log"
                )
            )
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    "Ajuram-Prasanna/CDK-Ajuram", "main",
                    authentication=SecretValue.unsafe_plain_text(self.response['SecretString'])
                ),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "npx cdk synth",
                ]
            ),
            code_build_defaults=pipelines.CodeBuildOptions(
                project=build_project
            )
        )
