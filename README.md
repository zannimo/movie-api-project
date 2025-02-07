# Movie API Project (Work in Progress) 🚧 

This project was created to demonstrate my skills in building a scalable and serverless application with AWS services using Boto3. 
The project showcases automation of infrastructure deployment and data handling, leveraging **AWS Lambda**, **API Gateway**, **S3**, and **DynamoDB** to build a simple yet powerful API that manages and serves movie data. 


## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [API Endpoints](#api-endpoints)
4. [Setup Instructions](#setup-instructions)
5. [Technologies Used](#technologies-used)
6. [Deployment](#deployment)
7. [Future Improvements](#future-improvements)

## Project Overview

This project demonstrates a serverless architecture using AWS services. It provides an API that allows users to:

- Retrieve a list of all movies.
- Fetch movies filtered by year.
- Retrieve detailed movie summaries (under development).


## Project Structure
The API infrastructure and its data is automatically set up using the following scripts: 

### `deploy_all.py`
This Python script automates the deployment of the following AWS infrastructure:
- **S3**: Used for storing static data.
- **DynamoDB**: Used to store movie metadata.
- **Lambda**: Function to process API requests.
- **API Gateway**: Exposes Lambda functions as HTTP endpoints.

Running this script will deploy the entire infrastructure needed for the project.

### `add-data-infra.py`
This Python script loads the initial data into S3 and DynamoDB. It interacts with the previously deployed infrastructure to populate the database and storage with movie data.

### Infrastructure Flow:
1. Run `deploy_all.py` to deploy all the AWS resources (S3, DynamoDB, Lambda, API Gateway).
2. Run `add-data-infra.py` to load sample movie data into S3 and DynamoDB.
3. Send API requests to test the infrastructure and see the responses.
4. When done, remember to destroy all infrastructure by running `destroy_all.py`.

## API Endpoints

### `GET /getmovies`
Returns a list of all movies.

**Response**:
```json
[
    {
        "movie_id": "1",
        "title": "Movie Title",
        "year": 2022
    },
    ...
]
```

### GET /getmoviesbyyear/{year}
Returns a list of movies released in the specified year.

**Response**:
```json
[
    {
        "movie_id": "1",
        "title": "Movie Title",
        "year": 2022
    },
    ...
]
```

### GET /getmoviesummary/{movie_id}
Returns a detailed summary for the movie identified by movie_id (this feature is under development).

## Setup Instructions
### Prerequisites:
- AWS CLI configured with the correct credentials.
- Python 3.x installed.

### Step-by-Step Setup:
Clone the repository:
```bash
git clone https://github.com/yourusername/movie-api-project.git
```

### Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

### Install the required dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

Deploy AWS Infrastructure: Run the deploy_all.py script to create the required AWS resources (S3, DynamoDB, Lambda, API Gateway):
```bash
python3 deploy_all.py
```

Load Data into DynamoDB and S3: Run the add-data-infra.py script to load movie data:
```bash
python3 add-data-infra.py
```
Test the API: Once the infrastructure is deployed and data is loaded, you can test the API using tools like curl or Postman.

For example:
```bash
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/getmovies
```

### Technologies Used
- AWS Lambda: Serverless compute service to run the functions.
- API Gateway: Manages API routes and invokes Lambda.
- Amazon DynamoDB: NoSQL database for storing movie data.
- Amazon S3: Used for storing static data such as movie assets or metadata.
- Python: The programming language used for Lambda functions and automation scripts.

### Deployment
The deploy_all.py script automates the deployment of infrastructure resources. It will create the necessary Lambda functions, S3 buckets, DynamoDB tables, and API Gateway routes.
The add-data-infra.py script populates DynamoDB and S3 with the movie data.
Once deployed, the API can be accessed through API Gateway.

### Future Improvements
Movie Summary Endpoint: Integrate with an AI service for detailed movie summaries.
Pagination: Add support for pagination to handle large data sets.
Authentication: Add user authentication to secure the API.
