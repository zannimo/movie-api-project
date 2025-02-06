import boto3
from utils import get_shared_value

# Set the AWS region
AWS_REGION = "us-east-1"
AWS_PROFILE = "movie-api-user"

# Ensure the profile is set (this will use the same profile as the main script)
session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)

# AWS Clients
lambda_client = boto3.client("lambda", region_name=AWS_REGION)

LAMBDA_FUNCTION_NAME = get_shared_value("lambda_function_name")

# Retrieve the three API Gateway URLs
API_GATEWAY_URL_GETMOVIES = get_shared_value("api_gateway_url_getmovies")
API_GATEWAY_URL_GETMOVIESBYYEAR = get_shared_value("api_gateway_url_getmoviesbyyear/{id}")
API_GATEWAY_URL_GETMOVIESUMMARY = get_shared_value("api_gateway_url_getmoviesummary/{id}")

# Create a dictionary of API Gateway URLs
api_gateway_urls = {
    "API_GATEWAY_URL_GETMOVIES": API_GATEWAY_URL_GETMOVIES,
    "API_GATEWAY_URL_GETMOVIESBYYEAR": API_GATEWAY_URL_GETMOVIESBYYEAR,
    "API_GATEWAY_URL_GETMOVIESUMMARY": API_GATEWAY_URL_GETMOVIESUMMARY
}

def update_lambda_environment(LAMBDA_FUNCTION_NAME, api_gateway_urls):
    """Updates the environment variables of an existing Lambda function."""

    # Get the current configuration of the Lambda function
    response = lambda_client.get_function_configuration(FunctionName=LAMBDA_FUNCTION_NAME)

    # Extract existing environment variables
    existing_env_vars = response.get("Environment", {}).get("Variables", {})

    # Update with the new API Gateway URLs dynamically
    for key, value in api_gateway_urls.items():
        existing_env_vars[key] = value

    # Update Lambda function configuration
    lambda_client.update_function_configuration(
        FunctionName=LAMBDA_FUNCTION_NAME,
        Environment={"Variables": existing_env_vars}
    )

    print(f"Updated Lambda '{LAMBDA_FUNCTION_NAME}' with API Gateway URLs.")


# Run the update function
update_lambda_environment(LAMBDA_FUNCTION_NAME, api_gateway_urls)
