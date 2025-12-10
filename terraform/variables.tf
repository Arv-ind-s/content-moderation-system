variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "content-moderation"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.11"
}

variable "lambda_memory_size" {
  description = "Lambda memory in MB (Free Tier: up to 3GB)"
  type        = number
  default     = 512  # Adequate for model inference
  
  validation {
    condition     = var.lambda_memory_size >= 128 && var.lambda_memory_size <= 1024
    error_message = "Keep memory <= 1024MB to stay within reasonable Free Tier usage"
  }
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds (Free Tier: 15 min max)"
  type        = number
  default     = 30
  
  validation {
    condition     = var.lambda_timeout <= 60
    error_message = "Keep timeout <= 60s to avoid unexpected costs"
  }
}

variable "s3_bucket_name" {
  description = "S3 bucket for model storage (Free Tier: 5GB)"
  type        = string
  default     = "content-moderation-models"
}

variable "dynamodb_table_name" {
  description = "DynamoDB table for prediction logs (Free Tier: 25GB)"
  type        = string
  default     = "moderation-predictions"
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days (Free Tier: 5GB)"
  type        = number
  default     = 7
}
