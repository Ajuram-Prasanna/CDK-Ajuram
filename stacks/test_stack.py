from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_codebuild as codebuild
    )
from constructs import Construct

class TestStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.test_log_group = logs.LogGroup(self, "TestLogGroup")
        self.logging=codebuild.LoggingOptions(
                    cloud_watch=codebuild.CloudWatchLoggingOptions(
                        enabled=True,
                        log_group=self.test_log_group,
                        prefix="test-log"
                    )
                )