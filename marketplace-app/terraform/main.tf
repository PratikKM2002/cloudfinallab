provider "aws" {
  region = "us-east-1"
}

# S3 Module
module "s3" {
  source      = "./modules/s3"
  environment = "production"
}

# RDS Module
module "rds" {
  source          = "./modules/rds"
  db_instance_id  = "marketplace-db"
  db_username     = "admin"
  db_password     = "adminpassword123"  # Should be managed securely, consider AWS Secrets Manager for production.
  db_name         = "marketplace"
  db_instance_type = "db.t3.micro"  # Change to the size that fits your use case
  db_engine        = "mysql"  # You can use "postgres" if you want PostgreSQL
}

# Lambda Module
module "lambda" {
  source               = "./modules/lambda"
  lambda_function_name = "UserManagementLambda"
  bucket_name          = module.s3.bucket_name  # Pass the bucket name from the s3 module

  # Pass environment variables for Lambda using outputs from RDS module
  RDS_HOST     = module.rds.db_endpoint
  RDS_USERNAME = module.rds.db_username
  RDS_PASSWORD = module.rds.db_password
  RDS_DB_NAME  = module.rds.db_name
}

# API Gateway Module
module "api_gateway" {
  source               = "./modules/api_gateway"
  api_name             = "MarketplaceAPI"
    lambda_function_arn  = module.lambda.lambda_function_arn  # Pass Lambda ARN here
  region               = var.region
}

