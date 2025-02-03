#!/bin/bash

AWS_REGION="us-east-1"
echo "AWS region: $AWS_REGION"

# Ensure the profile is set (this will use the same profile as the main script)
export AWS_PROFILE=movie-api-user

# Generate a unique bucket name
BUCKET_NAME="my-movie-covers-bucket-$(date +%s)"
echo "Creating S3 bucket: $BUCKET_NAME"
aws s3api create-bucket \
    --bucket $BUCKET_NAME \
    --region $AWS_REGION 

# Save the bucket name for future use
echo "$BUCKET_NAME" > bucket_name.txt

echo "S3 Bucket created successfully."
