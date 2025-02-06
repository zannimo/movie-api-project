#!/bin/bash

AWS_REGION="us-east-1"
echo "AWS region: $AWS_REGION"

# Ensure the profile is set (this will use the same profile as the main script)
export AWS_PROFILE=movie-api-user

echo "Creating DynamoDB Table..."
aws dynamodb create-table \
    --table-name Movies \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION

echo "Waiting for table to be active..."
aws dynamodb wait table-exists --table-name Movies --region $AWS_REGION

echo "DynamoDB Table created successfully."
