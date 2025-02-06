import json
import boto3
from botocore.exceptions import ClientError
import os
from decimal import Decimal

# Set the AWS region
AWS_REGION = "us-east-1"
AWS_PROFILE = "movie-api-user"

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

# Retrieve table name from environment variables
MOVIE_TABLE = os.environ.get("DYNAMODB_TABLE")

if not MOVIE_TABLE:
    raise ValueError("DYNAMODB_TABLE environment variable is not set.")

class JSONEncoder(json.JSONEncoder):
    """Custom JSONEncoder to handle DynamoDB Decimal types."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    # Initialize DynamoDB table
    table = dynamodb.Table(MOVIE_TABLE)

    try:
        # Query the DynamoDB table to get the list of movies
        response = table.scan()  # Returns a dictionary

        # Extract the items (movies) from the response
        movies = response.get('Items', [])

        # Construct image URLs if necessary (we assume 'cover_url' is already the full S3 URL)
        for movie in movies:
            cover_url = movie.get('cover_url', '')
            if cover_url:
                movie['cover_url'] = cover_url  # It's already a complete S3 URL

        # Return the list of movies in the response using the custom JSONEncoder
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Movies retrieved successfully',
                'movies': movies
            }, cls=JSONEncoder, indent=4),  # Use the custom JSONEncoder here
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except ClientError as e:
        print(f"Error fetching data: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to retrieve movies',
                'error': str(e)
            }, cls=JSONEncoder, indent=4),  # Use the custom JSONEncoder here
            'headers': {
                'Content-Type': 'application/json'
            }
        }
