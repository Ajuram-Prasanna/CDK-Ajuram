import boto3

secret_client = boto3.client('secretsmanager')

response = secret_client.get_secret_value(
    SecretId='arn:aws:secretsmanager:ap-southeast-1:682853212408:secret:cdk-token'
)

print(response['SecretString'])