import boto3
from botocore.exceptions import ClientError
from utils import update_shared_value

# Set the AWS region
AWS_REGION = "us-east-1"
AWS_PROFILE = "movie-api-user"

# Set up the session and DynamoDB client using the specified profile
session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
dynamodb = session.client("dynamodb")

# Create the DynamoDB table
def create_dynamodb_table():
    try:
        print("Creating DynamoDB Table...")

        response = dynamodb.create_table(
            TableName="Movies",
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"}
            ],
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print(f"Table creation initiated: {response}")

         # Write the dynamoDB_table_name to the JSON file

         # Create dict with new key-value pair that will be added to the JSON file.
        dynamoDB_table_name = {}
        dynamoDB_table_name["Table_name"] = response["TableDescription"]["TableName"] # It is a nested dictionary
        update_shared_value(dynamoDB_table_name)

    except ClientError as e:
        print(f"Error creating table: {e}")     
       

# Wait for the table to be active
def wait_for_table_to_be_active():
    print("Waiting for table to be active...")
    waiter = dynamodb.get_waiter("table_exists")
    try:
        waiter.wait(TableName="Movies")
        print("DynamoDB Table created successfully.")

    except ClientError as e:
        print(f"Error waiting for table: {e}")

# Run the functions
create_dynamodb_table()
wait_for_table_to_be_active()



