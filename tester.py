# import pytest
# import os

# for test_file in os.listdir('tests'):
#     if test_file.startswith('test_') and test_file.endswith('.py'):
#         result = pytest.main(['tests/' + test_file, '-q'])
#         if result == 0:
#             print("Passed")
#         else:
#             print("Failed")




import boto3

# Initialize boto3 client for Lambda
lambda_client = boto3.client('lambda', region_name='ap-southeast-1')

# Specify the function name, zip file path, and other parameters
function_name = 'lambda_function'
zip_file_path = 'lambdas/lambda_function.zip'
role_arn = 'arn:aws:iam::682853212408:role/cag-baggage-LambdaRole-bDBa4Q3CoVa4'
runtime = 'python3.9'
handler = 'lambda_function.lambda_handler'

# Read the zip file content
with open(zip_file_path, 'rb') as zip_file:
    zip_content = zip_file.read()

# Create or update the Lambda function
try:
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={'ZipFile': zip_content},
        Description='A sample Lambda function',
        Timeout=30,
        MemorySize=128,
        Publish=True
    )
    print("Lambda function created successfully:", response)
except lambda_client.exceptions.ResourceConflictException:
    response = lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_content,
        Publish=True
    )
    print("Lambda function updated successfully:", response)
