# variable "bucket_name" {
#   description = "The name of the S3 bucket"
#   type        = string
# }
variable "environment" {
  description = "The environment for the resources (e.g., dev, prod)"
  type        = string
  default     = "dev" # Replace with the appropriate default value
}
