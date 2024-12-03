output "s3_bucket_name" {
  value = module.s3.bucket_name
}

output "api_gateway_url" {
  value = module.api_gateway.invoke_url
}

output "lambda_function_arn" {
  value = module.lambda.lambda_arn
}
