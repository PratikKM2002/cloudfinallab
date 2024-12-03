variable "lambda_function_arn" {
  description = "The ARN of the Lambda function"
}


variable "api_name" {
  description = "Name of the API Gateway"
  type        = string
}

variable "region" {
  description = "The AWS region for the API Gateway"
}

