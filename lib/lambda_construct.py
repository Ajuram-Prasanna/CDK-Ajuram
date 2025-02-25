from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    custom_resources as cr,
)
from constructs import Construct
import os
import hashlib
import subprocess
import boto3
import tempfile
import shutil
import logging
import zipfile
import pytest



class LambdaDeploymentConstruct(Construct):
    def __init__(self, scope: Construct, id: str, lambda_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.lambda_client = boto3.client('lambda', region_name='ap-southeast-1')
        self.role_arn = 'arn:aws:iam::682853212408:role/cag-baggage-LambdaRole-bDBa4Q3CoVa4'
        self.runtime = 'python3.9'

        try:
            self.delete_function(lambda_name)
        except:
            pass

        if os.path.exists(f'lambdas/{lambda_name}/requirements.txt'):
            subprocess.check_call(['pip', 'install', '-r' f'lambdas/{lambda_name}/requirements.txt', '--target', f'lambdas/{lambda_name}'])
        if os.path.isdir(f'lambdas/{lambda_name}/tests'):
            status = True
            for test_file in os.listdir(f'lambdas/{lambda_name}/tests'):
                if pytest.main([f'lambdas/{lambda_name}/tests/{test_file}', '-q']) == 1:
                    status = False
                    break
            if status:
                zip_file_path = f'lambdas/{lambda_name}.zip'
                self.zip_folder(f'lambdas/{lambda_name}', zip_file_path)
                self.upload(zip_file_path, lambda_name)
        else:
            zip_file_path = f'lambdas/{lambda_name}.zip'
            self.zip_folder(f'lambdas/{lambda_name}', zip_file_path)
            self.upload(zip_file_path, lambda_name)
    
    def delete_function(self, function_name):
            try:
                self.lambda_client.delete_function(FunctionName=function_name)
                print(f"Deleted existing function: {function_name}")
            except self.lambda_client.exceptions.ResourceNotFoundException:
                print(f"Function does not exist: {function_name}")
            except Exception as e:
                print(f"Error deleting function: {function_name}, {e}")


    def zip_folder(self, folder_path, output_zip_path):
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)

    def upload(self, zip_file_path, lambda_function):
        with open(zip_file_path, 'rb') as zip_file:
            zip_content = zip_file.read()
        # Create or update the Lambda function
        try:
            response = self.lambda_client.create_function(
                FunctionName=lambda_function,
                Runtime=self.runtime,
                Role=self.role_arn,
                Handler=f'{lambda_function}.lambda_handler',
                Code={'ZipFile': zip_content},
                Description=f'Lambda function - {lambda_function}',
                Timeout=30,
                MemorySize=128,
                Publish=True
            )
            print("Lambda function created successfully:", response)
        except self.lambda_client.exceptions.ResourceConflictException:
            response = self.lambda_client.update_function_code(
                FunctionName=lambda_function,
                ZipFile=zip_content,
                Publish=True
            )
            print("Lambda function updated successfully:", response)
        except:
            pass
