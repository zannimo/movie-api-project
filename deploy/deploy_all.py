import subprocess

# Run deploy_s3.py 
print("deploy_s3.py started")
subprocess.run(['python3', 'deploy_s3.py'])
print("deploy_s3.py done")

# Run deploy_dynamodb.py 
print("deploy_dynamodb.py started")
subprocess.run(['python3', 'deploy_dynamodb.py'])
print("deploy_dynamodb.py done")

# Run deploy_lambda.py
print("deploy_lambda.py started")
subprocess.run(['python3', 'deploy_lambda.py'])
print("deploy_lambda.py done")

# Run deploy_api_gateway.py
print("deploy_api_gateway started")
subprocess.run(['python3', 'deploy_api_gateway.py'])
print("deploy_api_gateway.py done")

# Run update_lambda_env_variable.py
print("update_lambda_env_variable.py started")
subprocess.run(['python3', 'update_lambda_env_variable.py'])
print("update_lambda_env_variable.py done")


