from aws_cdk import Stage
from constructs import Construct
from stacks.test_stack import TestStack

class TestStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        TestStack(self, "TestStack")