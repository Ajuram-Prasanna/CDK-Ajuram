from aws_cdk import (Stage,
                     pipelines as pipelines,
                     aws_logs as logs,
                     aws_codebuild as codebuild
                     )
from constructs import Construct
from stacks.test_stack import TestStack

class TestStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        TestStack(self, "TestStack")

        test_log_group = logs.LogGroup(self, "TestLogGroup",
                                       retention=logs.RetentionDays.ONE_WEEK)

        # Define the CodeBuildStep with the testing commands
        testing_step = pipelines.CodeBuildStep(
            "RunTests",
            commands=[
                "pip install -r requirements.txt",  # Ensure dependencies are installed
                "python tester.py"  # Run tests using pytest
            ],
            logging=codebuild.LoggingOptions(
                cloud_watch=codebuild.CloudWatchLoggingOptions(
                    enabled=True,
                    log_group=test_log_group,
                    prefix="test-log"
                )
            )
        )