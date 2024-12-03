variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
}



variable "RDS_HOST" {
  description = "The endpoint of the RDS instance"
  type        = string
}

variable "RDS_USERNAME" {
  description = "The username for the RDS instance"
  type        = string
}

variable "RDS_PASSWORD" {
  description = "The password for the RDS instance"
  type        = string
}

variable "RDS_DB_NAME" {
  description = "The database name"
  type        = string
}
