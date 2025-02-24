import os
import zipfile
import boto3
import pytest

lambda_client = boto3.client('lambda', region_name='ap-southeast-1')
role_arn = 'arn:aws:iam::682853212408:role/cag-baggage-LambdaRole-bDBa4Q3CoVa4'
runtime = 'python3.9'

def zip_folder(folder_path, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)


def upload(zip_file_path):
    with open(zip_file_path, 'rb') as zip_file:
        zip_content = zip_file.read()
    # Create or update the Lambda function
    try:
        response = lambda_client.create_function(
            FunctionName=lambda_function,
            Runtime=runtime,
            Role=role_arn,
            Handler=f'{lambda_function}.lambda_handler',
            Code={'ZipFile': zip_content},
            Description=f'Lambda function - {lambda_function}',
            Timeout=30,
            MemorySize=128,
            Publish=True
        )
        print("Lambda function created successfully:", response)
    except lambda_client.exceptions.ResourceConflictException:
        response = lambda_client.update_function_code(
            FunctionName=lambda_function,
            ZipFile=zip_content,
            Publish=True
        )
        print("Lambda function updated successfully:", response)

for lambda_function in os.listdir('lambdas'):
    if os.path.isdir(f'lambdas/{lambda_function}/tests'):
        status = True
        for test_file in os.listdir(f'lambdas/{lambda_function}/tests'):
            if pytest.main([f'lambdas/{lambda_function}/tests/{test_file}', '-q']) == 1:
                status = False
                break
        if status:
            zip_file_path = f'lambdas/{lambda_function}.zip'
            zip_folder(f'lambdas/{lambda_function}', zip_file_path)
            upload(zip_file_path)
    else:
        zip_file_path = f'lambdas/{lambda_function}.zip'
        zip_folder(f'lambdas/{lambda_function}', zip_file_path)
        upload(zip_file_path)
