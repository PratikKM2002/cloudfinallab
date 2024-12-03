resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "bucket" {
  bucket = "marketplace-app-bucket-${random_id.bucket_suffix.hex}"
  tags = {
    Environment = var.environment
  }
}

# Versioning Configuration
resource "aws_s3_bucket_versioning" "bucket_versioning" {
  bucket = aws_s3_bucket.bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Restrict Public Access Configuration
resource "aws_s3_bucket_public_access_block" "public_access_block" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
