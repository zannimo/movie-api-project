import boto3
import csv
import os
import uuid
import sys

# Get the absolute path of the parent directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # movie-api-project/play
parent_dir = os.path.dirname(script_dir)  # movie-api-project
deploy_dir = os.path.join(parent_dir, "deploy")  # movie-api-project/deploy

# Add deploy directory to sys.path
sys.path.append(deploy_dir)

# Now you can import utils
from utils import get_shared_value

# AWS Configurations
BUCKET_NAME = get_shared_value("s3_bucket_name")
DYNAMODB_TABLE = get_shared_value("Table_name")
AWS_REGION = "us-east-1"  # Example: 'us-east-1'

# AWS Clients
s3_client = boto3.client("s3", region_name=AWS_REGION) # Lower level API 
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION) # Higher level API
table = dynamodb.Table(DYNAMODB_TABLE)

# Function to upload file to S3 and return its public URL
def upload_to_s3(local_path): # the argument for "local-path" will be the value under "cover_file" in the csv file. 
    filename = os.path.basename(local_path)  # Extract filename only
    s3_client.upload_file(local_path, BUCKET_NAME, filename)  
    return f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"

# Read and process CSV file
csv_file = "movies.csv"

with open(csv_file, mode="r", encoding="utf-8") as file: # Opens the CSV file for reading
    reader = csv.DictReader(file) # Reads the file and creates a dictionary for each row. "reader" becomes an iterator over those dictionaries
    
    for row in reader: # Loops through the dictionaries, processing each row
        cover_file = row["cover_file"]  # Example: 'images/inception.jpg'
        
        # Ensure the image file exists before uploading
        if not os.path.exists(cover_file):
            print(f"Error: File {cover_file} not found!")
            continue
        
        # Upload image and get the S3 URL, calling the function earlier defined
        s3_url = upload_to_s3(cover_file)
        
        # Insert into DynamoDB (excluding 'cover_file' and adding 'cover_url')
        item = {
            "id": str(uuid.uuid4()),
            "title": row["title"],
            "year": int(row["year"]),
            "genre": row["genre"],
            "cover_url": s3_url,  # Replacing local path with S3 URL
        }

        table.put_item(Item=item)
        print(f"Uploaded {row['title']} successfully!")
