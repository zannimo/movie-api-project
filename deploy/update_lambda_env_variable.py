import boto3
from utils import get_shared_value

# Set the AWS region
AWS_REGION = "us-east-1"
AWS_PROFILE = "movie-api-user"

# Ensure the profile is set (this will use the same profile as the main script)
session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)

# AWS Clients
lambda_client = boto3.client("lambda",region_name=AWS_REGION)

LAMBDA_FUNCTION_NAME = get_shared_value("lambda_function_name")
API_GATEWAY_URL = get_shared_value("api_gateway_url")

def update_lambda_environment(LAMBDA_FUNCTION_NAME, API_GATEWAY_URL):
    """Updates the environment variables of an existing Lambda function."""

    # Get the current configuration of the Lambda function
    response = lambda_client.get_function_configuration(FunctionName=LAMBDA_FUNCTION_NAME)

    # Extract existing environment variables
    existing_env_vars = response.get("Environment", {}).get("Variables", {})

    # Update with new API Gateway URL
    existing_env_vars["API_GATEWAY_URL"] = API_GATEWAY_URL

    # Update Lambda function configuration
    lambda_client.update_function_configuration(
        FunctionName=LAMBDA_FUNCTION_NAME,
        Environment={"Variables": existing_env_vars}
    )

    print(f"Updated Lambda '{LAMBDA_FUNCTION_NAME}' with API Gateway URL: {API_GATEWAY_URL}")

# Run the update function
update_lambda_environment(LAMBDA_FUNCTION_NAME, API_GATEWAY_URL)
