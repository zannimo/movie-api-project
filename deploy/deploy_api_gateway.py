import boto3
from utils import update_shared_value

# Set the AWS region
AWS_REGION = "us-east-1"
AWS_PROFILE = "movie-api-user"

session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)

# Get the current AWS account ID using STS
sts_client = boto3.client('sts')
account_id = sts_client.get_caller_identity()['Account']

# AWS clients
apigateway = boto3.client('apigatewayv2',region_name=AWS_REGION)
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

# Define API Gateway name
api_name = "MoviesAPI"

# Step 1: Create API Gateway
response = apigateway.create_api(
    Name=api_name,
    ProtocolType='HTTP'
)
api_id = response['ApiId']
print(f"API Gateway created: {api_id}")

# Step 2: Create a Lambda integration (before the route)
lambda_arn = f"arn:aws:lambda:{AWS_REGION}:{account_id}:function:GetMovies"  # Replace with actual ARN

integration_response = apigateway.create_integration(
    ApiId=api_id,
    IntegrationType="AWS_PROXY",
    IntegrationUri=lambda_arn,
    PayloadFormatVersion="2.0"
)
integration_id = integration_response['IntegrationId']
print(f"Integration created: {integration_id}")


# Step 3: Create a route (GET /movies) and attach integration
route_response = apigateway.create_route(
    ApiId=api_id,
    RouteKey="GET /movies",
    Target=f"integrations/{integration_id}"
)
route_id = route_response['RouteId']
print(f"Route created: GET /movies ({route_id})")


# Step 4: Create a stage (AutoDeploy=True means no manual deployment - create.deployment() - is needed)
stage_name = "prod"
stage_response = apigateway.create_stage(
    ApiId=api_id,
    StageName=stage_name,
    AutoDeploy=True  # Ensures new changes are automatically deployed
)
print(f"Stage {stage_name} created.")

# Save the api_gateway_url to the JSON file

api_gateway_url = {"api_gateway_url":f"https://{api_id}.execute-api.{AWS_REGION}.amazonaws.com/{stage_name}/movies"}
update_shared_value(api_gateway_url)

print(f"API Gateway deployed at: {api_gateway_url['api_gateway_url']}")


# Step 6: Grant API Gateway permission to invoke Lambda
lambda_client.add_permission(
    FunctionName="GetMovies",
    StatementId="AllowAPIGatewayInvoke",
    Action="lambda:InvokeFunction",
    Principal="apigateway.amazonaws.com",
    SourceArn=f"arn:aws:execute-api:{AWS_REGION}:{account_id}:{api_id}/*/*/movies"
)

print("API Gateway setup complete!")
