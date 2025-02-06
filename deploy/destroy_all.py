import boto3
from utils import get_shared_value

# Initialize AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.client("dynamodb")
lambda_client = boto3.client("lambda")
apigateway = boto3.client("apigateway")

# Retrieving the names of the resources:
s3_bucket_name = get_shared_value("s3_bucket_name")
dynamodb_table_name = get_shared_value("Table_name")
lambda_function_name = get_shared_value("lambda_function_name")


# Function to delete all objects in an S3 bucket before deleting it
def delete_s3_bucket(s3_bucket_name):
    try:
        # Delete all objects in the bucket
        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(s3_bucket_name)
        bucket.objects.all().delete()
        print(f"Deleted all objects in {s3_bucket_name}")

        # Delete the bucket itself
        s3.delete_bucket(Bucket=s3_bucket_name)
        print(f"Deleted S3 bucket: {s3_bucket_name}")
    except Exception as e:
        print(f"Error deleting S3 bucket {s3_bucket_name}: {e}")

# Function to delete a DynamoDB table
def delete_dynamodb_table(dynamodb_table_name):
    try:
        dynamodb.delete_table(TableName=dynamodb_table_name)
        print(f"Deleted DynamoDB table: {dynamodb_table_name}")
    except Exception as e:
        print(f"Error deleting DynamoDB table {dynamodb_table_name}: {e}")

# Function to delete a Lambda function
def delete_lambda_function(function_name):
    try:
        lambda_client.delete_function(FunctionName=function_name)
        print(f"Deleted Lambda function: {function_name}")
    except Exception as e:
        print(f"Error deleting Lambda function {function_name}: {e}")

# Function to delete all HTTP API Gateway resources
def delete_api_gateway():
    try:
        apigateway_v2 = boto3.client("apigatewayv2")  # Use API Gateway v2 client

        # Get all HTTP APIs
        response = apigateway_v2.get_apis()
        for api in response["Items"]:
            api_id = api["ApiId"]
            api_name = api.get("Name", "Unnamed API")  # Some APIs may not have a name
            print(f"Deleting API Gateway: {api_name} (ID: {api_id})")
            apigateway_v2.delete_api(ApiId=api_id)

        print("Deleted all HTTP APIs.")
    except Exception as e:
        print(f"Error deleting API Gateway: {e}")

# Execute deletions
delete_s3_bucket(s3_bucket_name)
delete_dynamodb_table(dynamodb_table_name)
delete_lambda_function(lambda_function_name)
delete_api_gateway()

print("All specified resources deleted.")
