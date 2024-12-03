resource "aws_lambda_function" "lambda" {
  function_name = var.lambda_function_name
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"
   filename      = "/home/pratikkm02/home/pratikkm02/cloudfinalproject/marketplace-app/backend/user_management/lambda_function.zip"  # Correct path to your zip file
  role          = aws_iam_role.lambda_execution_role.arn

  environment {
    variables = {
      BUCKET_NAME   = var.bucket_name      # S3 bucket name
      RDS_HOST      = var.RDS_HOST         # RDS connection details
      RDS_USERNAME  = var.RDS_USERNAME
      RDS_PASSWORD  = var.RDS_PASSWORD
      RDS_DB_NAME   = var.RDS_DB_NAME
    }
  }

  depends_on = [aws_iam_role.lambda_execution_role]
}


resource "aws_iam_role" "lambda_execution_role" {
  name               = "${var.lambda_function_name}-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "s3_access_policy" {
  name        = "${var.lambda_function_name}-s3-access"
  description = "Policy to allow Lambda function to access S3 bucket"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_access" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

resource "aws_iam_policy" "rds_access_policy" {
  name        = "${var.lambda_function_name}-rds-access"
  description = "Policy to allow Lambda function to access RDS"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "rds:DescribeDBInstances",
          "rds:Connect"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_rds_access" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.rds_access_policy.arn
}
