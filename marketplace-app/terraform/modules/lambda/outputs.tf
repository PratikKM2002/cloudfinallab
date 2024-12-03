output "lambda_arn" {
  value = aws_lambda_function.lambda.arn
}

# variables.tf in the lambda module
variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}
output "lambda_function_arn" {
  value = aws_lambda_function.lambda.arn
}
