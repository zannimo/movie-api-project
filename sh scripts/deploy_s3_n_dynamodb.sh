#!/bin/bash

# Set the profile to use for AWS CLI commands
export AWS_PROFILE=movie-api-user

set -e  # Exit on error

echo "Setting up AWS Infrastructure..."

# Create DynamoDB Table
./create_dynamodb.sh

# Create S3 Bucket
./create_s3.sh

echo "AWS Infrastructure setup complete."

