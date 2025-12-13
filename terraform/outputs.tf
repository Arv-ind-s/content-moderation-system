output "s3_bucket_name" {
  description = "Name of the S3 bucket for model storage"
  value       = aws_s3_bucket.model_storage.id
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.predictions.name
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.moderation_api.function_name
}

output "api_endpoint" {
  description = "HTTP API Gateway Endpoint URL"
  value       = aws_apigatewayv2_stage.default.invoke_url
}
