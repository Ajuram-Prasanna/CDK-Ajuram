from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_codebuild as codebuild
    )
from constructs import Construct
import subprocess

class TestStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)