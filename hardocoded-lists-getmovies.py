import json

def lambda_handler(event, context):
    movies = [
        {"title": "Inception", "year": 2010, "cover_url": "https://example.com/inception.jpg"},
        {"title": "Interstellar", "year": 2014, "cover_url": "https://example.com/interstellar.jpg"}
    ]
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(movies)
    }
