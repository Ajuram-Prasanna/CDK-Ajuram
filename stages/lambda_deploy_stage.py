from aws_cdk import Stage
from constructs import Construct
import aws_cdk.aws_lambda as _lambda

class LambdaDeployStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset(r"C:\Users\Ajuramprasanna\Desktop\CDK-Ajuram\stages\lambda_deploy_stage.py")
        )