from aws_cdk import Stage
from constructs import Construct
from stacks.prod_deploy_stack import ProdDeployStack

class ProdDeployStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        ProdDeployStack(self, "TestStack")
