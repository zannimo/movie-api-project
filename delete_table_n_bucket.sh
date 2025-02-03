#!/bin/bash

TABLE_NAME=Movies 
BUCKET_NAME=my-movie-covers-bucket-1738599365

echo "Deleting table $TABLE_NAME and bucket $BUCKET_NAME..."

# Delete the table
aws dynamodb delete-table --table-name $TABLE_NAME --region us-east-1 --profile movie-api-user

# Delete all objects inside the bucket
aws s3 rm s3://$BUCKET_NAME --recursive --region us-east-1 --profile movie-api-user

# Delete the bucket
aws s3api delete-bucket --bucket $BUCKET_NAME --region us-east-1 --profile movie-api-user

echo Deleted both!