from aws_cdk import (
    SecretValue,
    Stack,
    aws_codebuild as codebuild,
    aws_iam as iam,
    aws_logs as logs,
    Stage
)
import os
from constructs import Construct
from aws_cdk.pipelines import CodePipelineSource
import boto3

from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines as pipelines,
)

from aws_cdk.pipelines import CodePipelineSource, CodePipeline, CodeBuildOptions, CodeBuildStep

from stages.prod_deploy_stage import ProdDeployStage

from lib.lambda_construct import LambdaDeploymentConstruct

from aws_cdk.pipelines import ManualApprovalStep

from time import time

def caesar_encrypt(text, shift):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

class CdkSampleStack(Stack):
    def __init__(self, scope: Construct, id: str, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        

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
            ),
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml")
        )



        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            pipeline_name="AjuramPipelineNew",
            synth=pipelines.ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    "Ajuram-Prasanna/CDK-Ajuram", "main",
                    authentication=SecretValue.unsafe_plain_text(caesar_decrypt("jlwkxe_sdw_11ESQTXIT040BHq4oIWUz9_XfLydeATto7nCvUeNsdUygSqmC5FQ1ttMuT1BSULW2bT4FMSGE6ZME4g6LA", 3))
                ),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "npx cdk synth",
                ]
            ),
            code_build_defaults=pipelines.CodeBuildOptions(
                logging=codebuild.LoggingOptions(
                    cloud_watch=codebuild.CloudWatchLoggingOptions(
                        enabled=True,
                        log_group=log_group,
                        prefix="build-log"
                    )
                )
            )
        )

        prod_deploy_stage = ProdDeployStage(self, "ProdDeployStage")

        log_group = logs.LogGroup(self, "ApprovalLogGroup")

        log_group.add_stream("ApprovalLogStream")

        pipeline.add_stage(prod_deploy_stage,
            pre=[pipelines.ManualApprovalStep("PromoteToProd")]
        )
        