variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "api_name" {
  description = "Name of the API Gateway"
  type        = string
}

variable "region" {
  description = "The AWS region where resources will be deployed"
  default     = "us-east-1"  # Set your desired AWS region
}
