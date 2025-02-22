from aws_cdk import Stack
from constructs import Construct

class TestStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Define resources needed for the test stage here, if any