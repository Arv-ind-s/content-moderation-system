output "s3_bucket_name" {
  description = "Name of the S3 bucket for model storage"
  value       = aws_s3_bucket.model_storage.id
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.predictions.name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.moderation_api.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.moderation_api.function_name
}

output "iam_role_arn" {
  description = "ARN of the IAM role for Lambda"
  value       = aws_iam_role.lambda_role.arn
}

output "deployment_info" {
  description = "Deployment information and cost controls"
  value = {
    free_tier_compliant = "Yes - All resources within Free Tier limits"
    estimated_cost      = "$0.00 for first 12 months (within Free Tier)"
    log_retention       = "${var.log_retention_days} days"
    auto_cleanup        = "Enabled for logs and old data"
  }
}
