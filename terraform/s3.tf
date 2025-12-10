resource "aws_s3_bucket" "model_storage" {
  bucket = "${var.s3_bucket_name}-${var.environment}-${data.aws_caller_identity.current.account_id}"
  
  tags = {
    Name        = "Model Storage"
    CostCenter  = "Free Tier"
    AutoCleanup = "true"
  }
}

# REMOVED VERSIONING - Saves storage space (Free Tier = 5GB total)
# Versioning would duplicate the 268MB model file

resource "aws_s3_bucket_server_side_encryption_configuration" "model_storage" {
  bucket = aws_s3_bucket.model_storage.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"  # Free, no KMS costs
    }
  }
}

resource "aws_s3_bucket_public_access_block" "model_storage" {
  bucket = aws_s3_bucket.model_storage.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle policy to auto-delete old objects (cost control)
resource "aws_s3_bucket_lifecycle_configuration" "model_storage" {
  bucket = aws_s3_bucket.model_storage.id
  
  rule {
    id     = "delete-old-logs"
    status = "Enabled"
    
    # Delete any logs older than 7 days
    filter {
      prefix = "logs/"
    }
    
    expiration {
      days = 7
    }
  }
}

# Get current AWS account ID for unique bucket name
data "aws_caller_identity" "current" {}
