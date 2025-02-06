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
lambda_arn = f"arn:aws:lambda:{AWS_REGION}:{account_id}:function:GetMovies"  

integration_response = apigateway.create_integration(
    ApiId=api_id,
    IntegrationType="AWS_PROXY",
    IntegrationUri=lambda_arn,
    PayloadFormatVersion="2.0"
)
integration_id = integration_response['IntegrationId']
print(f"Integration created: {integration_id}")


# Step 3: Create routes and attach integration
routes_config = [
    {"route_key": "GET /getmovies"},
    {"route_key": "GET /getmoviesbyyear/{id}"},
    {"route_key": "GET /getmoviesummary/{id}"}
]

for route in routes_config:
    route_response = apigateway.create_route(
        ApiId=api_id,
        RouteKey=route["route_key"],
        Target=f"integrations/{integration_id}"
    )
    print(f"Route created: {route['route_key']}")


# Step 4: Create a stage (AutoDeploy=True means no manual deployment - create.deployment() - is needed)
stage_name = "prod"
stage_response = apigateway.create_stage(
    ApiId=api_id,
    StageName=stage_name,
    AutoDeploy=True  # Ensures new changes are automatically deployed
)
print(f"Stage {stage_name} created.")

# Step 5: Save API Gateways URLs to shared file
# 5.1. Define the routes and their respective path templates
routes_list = [
    {"name": "getmovies", "path": "/getmovies"},
    {"name": "getmoviesbyyear/{id}", "path": "/getmoviesbyyear/{id}"},
    {"name": "getmoviesummary/{id}", "path": "/getmoviesummary/{id}"}
]

# 5.2. Loop through routes and generate the URLs, then update shared values with unique keys
for route in routes_list:
    route_name = route.get("name")  # Use .get() to avoid KeyError
    route_path = route.get("path")

    api_url_key = f"api_gateway_url_{route_name}"
    api_url_value = f"https://{api_id}.execute-api.{AWS_REGION}.amazonaws.com/{stage_name}{route_path}"
   
   # Update shared values (ensure it accumulates instead of overwriting)
    update_shared_value({api_url_key: api_url_value})

    print(f"API Gateway deployed at: {api_url_value}")


# Step 6: Grant API Gateway permission to invoke Lambda
lambda_client.add_permission(
    FunctionName="GetMovies",
    StatementId="AllowAPIGatewayInvoke",
    Action="lambda:InvokeFunction",
    Principal="apigateway.amazonaws.com",
    SourceArn=f"arn:aws:execute-api:{AWS_REGION}:{account_id}:{api_id}/*/*"
)

print("API Gateway setup complete!")
