# Define AWS Provider
provider "aws" {
  region = "us-west-2"  # Change to your preferred region
}

# S3 Bucket for storing movie cover images
resource "aws_s3_bucket" "movie_covers" {
  bucket = "movie-cover-images-bucket-unique-name"  # Change to a globally unique name
}

# DynamoDB Table for storing movie data
resource "aws_dynamodb_table" "movie_data" {
  name           = "Movies"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "title"

  attribute {
    name = "title"
    type = "S"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name               = "lambda-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda Function for GetMovies
resource "aws_lambda_function" "get_movies" {
  function_name = "GetMoviesFunction"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  filename      = "lambda_function.zip"  # Update with actual ZIP file path

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.movie_data.name
    }
  }
}

# IAM Policy for Lambda to Access S3 and DynamoDB
resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda-access-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "dynamodb:Scan"
        Resource = aws_dynamodb_table.movie_data.arn
        Effect   = "Allow"
      },
      {
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.movie_covers.arn}/*"
        Effect   = "Allow"
      }
    ]
  })
}

# API Gateway to expose the Lambda function as a REST API
resource "aws_apigatewayv2_api" "movie_api" {
  name          = "MovieAPI"
  protocol_type = "HTTP"
}

# API Gateway Integration with Lambda
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.movie_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.get_movies.invoke_arn
}

# API Gateway Route (GET /movies)
resource "aws_apigatewayv2_route" "get_movies_route" {
  api_id    = aws_apigatewayv2_api.movie_api.id
  route_key = "GET /movies"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# API Gateway Deployment
resource "aws_apigatewayv2_stage" "dev_stage" {
  api_id      = aws_apigatewayv2_api.movie_api.id
  name        = "dev"
  auto_deploy = true
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_movies.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.movie_api.execution_arn}/*/*"
}
