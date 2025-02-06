import boto3
import zipfile
import io
import json
from utils import update_shared_value 
from utils import get_shared_value

# Set the AWS region
AWS_REGION = "us-east-1"
AWS_PROFILE = "movie-api-user"

session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)

# Get the current AWS account ID using STS
sts_client = boto3.client('sts')
account_id = sts_client.get_caller_identity()['Account']

# Initialize boto3 clients for Lambda, IAM, and DynamoDB
lambda_client = boto3.client('lambda', region_name=AWS_REGION)
iam_client = boto3.client('iam', region_name=AWS_REGION)
dynamodb_client = boto3.client('dynamodb', region_name=AWS_REGION)

# Step 1: Read your Lambda function code from an existing Python file (lambda_function.py)
with open('lambda_function.py', 'rb') as f:
    lambda_code = f.read()

# Step 2: Create a ZIP file containing the function code
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.writestr('lambda_function.py', lambda_code)
zip_buffer.seek(0)
print("File zipped succesfully")

# Step 3: Create an IAM role with the necessary permissions (if it doesn't exist already)
role_name = 'MyLambdaExecutionRole'

# Trust relationship for Lambda to assume the role
role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }
    ]
}

try:
    response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(role_policy),
        Description='IAM Role for Lambda function'
    )
    print(f'Role {role_name} created successfully')
except iam_client.exceptions.EntityAlreadyExistsException:
    print(f'Role {role_name} already exists.')

# Attach the necessary permissions to the Lambda role
iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)
iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
)
iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn='arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess'
)

print("Role and permissions set")

# Step 4: Create the Lambda function using boto3
role_arn = role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

# Step 5: Set environment variables for Lambda (DynamoDB table, API Gateway URL, etc.)

environment_variables = {
    'DYNAMODB_TABLE': get_shared_value("Table_name"),
    'API_GATEWAY_URL': ''
}

response = lambda_client.create_function(
    FunctionName='GetMovies',  # Function name
    Runtime='python3.8',  # Lambda runtime environment
    Role=role_arn,  # IAM role ARN
    Handler='lambda_function.lambda_handler',  # The function entry point
    Code={
        'ZipFile': zip_buffer.read()  # Pass the ZIP file
    },
    Timeout=30,  # Optional: Set the timeout for the function
    MemorySize=128,  # Optional: Set the memory size
    Environment={
        'Variables': environment_variables  # Set environment variables
    }
)

# Write the Lambda function name to the JSON file
lambda_function_name = {}
lambda_function_name["lambda_function_name"] = response['FunctionName']

# Save the lambda function name for future use
update_shared_value(lambda_function_name)


print(f"Lambda function {response['FunctionName']} created successfully!")

# Step 6: Set up API Gateway to trigger Lambda (this is a manual step or can be automated)
# You can use the AWS CLI or API Gateway SDK to set up a trigger between API Gateway and Lambda

