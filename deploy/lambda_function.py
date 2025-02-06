import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
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
    
def get_all_movies(table):
    """Retrieve all movies from DynamoDB."""
    try:
        response = table.scan()
        movies = response.get("Items", [])

        # Ensure cover_url is formatted correctly
        for movie in movies:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Movies retrieved successfully", "movies": movies}, cls=JSONEncoder, indent=4),
                "headers": {"Content-Type": "application/json"},
            }
    
    except ClientError as e:
        return error_response("Failed to retrieve movies", e)

def get_movies_by_year(table, year): 
    """Retrieve movies filtered by year."""
    try:
        response = table.scan(
    FilterExpression = boto3.dynamodb.conditions.Attr("year").eq(int(year))
)
        movies = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Movies from year {year} retrieved successfully", "movies": movies}, cls=JSONEncoder, indent=4),
            "headers": {"Content-Type": "application/json"},
        }

    except ClientError as e:
        return error_response(f"Failed to retrieve movies from year {year}", e)

def get_movie_summary(table, movie_id):
    """Retrieve a single movie summary."""
    try:
        response = table.get_item(Key={"id": movie_id})
        movie = response.get("Item")

        if not movie:
            return {"statusCode": 404, "body": json.dumps({"message": "Movie not found"}), "headers": {"Content-Type": "application/json"}}

        summary = {
            "id": movie["id"],
            "title": movie["title"],
            "year": movie["year"],
            "summary": movie.get("summary", "No summary available"), 
        }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Movie summary retrieved successfully", "movie": summary}, cls=JSONEncoder, indent=4),
            "headers": {"Content-Type": "application/json"},
        }

    except ClientError as e:
        return error_response(f"Failed to retrieve movie summary for ID {movie_id}", e)

def error_response(message, exception):
    """Return a standardized error response."""
    print(f"Error: {message}: {exception}")
    return {
        "statusCode": 500,
        "body": json.dumps({"message": message, "error": str(exception)}, cls=JSONEncoder, indent=4),
        "headers": {"Content-Type": "application/json"},
    }

def lambda_handler(event, context):
    """Main Lambda function handler."""
    print(f"Full event: {json.dumps(event)}")  # Debugging line
    table = dynamodb.Table(MOVIE_TABLE)

    # Extract the API route and path parameters
    path = event.get("rawPath", "")  # This contains the API Gateway route
    path_params = event.get("pathParameters", {})

    print(f"Received path: {path}")  # Debugging line
    print(f"Received path parameters: {path_params}")  # Debugging line

    # Remove API Gateway stage prefix if present
    if path.startswith("/prod/"):
        path = "/" + path[len("/prod/"):]
    
    print(f"Adjusted path: {path}")

    if path == "/getmovies":
        return get_all_movies(table)
    
    elif path.startswith("/getmoviesbyyear/"):
        year = path_params.get("id")  # Extract year from path parameters
        if not year:
            return {"statusCode": 400, "body": json.dumps({"message": "Year parameter is missing"}), "headers": {"Content-Type": "application/json"}}
        return get_movies_by_year(table, year)
    
    elif path.startswith("/getmoviesummary/"):
        movie_id = path_params.get("id")  # Extract movie_id from path parameters
        if not movie_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Movie ID is missing"}), "headers": {"Content-Type": "application/json"}}
        return get_movie_summary(table, movie_id)

    return {"statusCode": 404, "body": json.dumps({"message": "Route not found"}), "headers": {"Content-Type": "application/json"}}






