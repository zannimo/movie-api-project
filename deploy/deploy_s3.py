import boto3
import time
from utils import update_shared_value

# Set the AWS region
AWS_REGION = "us-east-1"
AWS_PROFILE = "movie-api-user"

# Ensure the profile is set (this will use the same profile as the main script)
session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)

# Create an S3 client
s3_client = session.client("s3")

# Generate a unique bucket name
BUCKET_NAME = f"my-movie-covers-bucket-{int(time.time())}"
print(f"Creating S3 bucket: {BUCKET_NAME}")

# Create the S3 bucket
s3_client.create_bucket(
    Bucket=BUCKET_NAME,
)

# Save the bucket name for future use
s3_bucket_name = {"s3_bucket_name":BUCKET_NAME}
update_shared_value(s3_bucket_name)


print("S3 Bucket created successfully.")
