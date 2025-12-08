# Placeholder - actual Lambda function will be added after FastAPI development
resource "aws_lambda_function" "moderation_api" {
  filename      = "lambda_function.zip"  # Will be created in Step 6
  function_name = "${var.project_name}-api-${var.environment}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.handler"
  runtime       = var.lambda_runtime
  memory_size   = var.lambda_memory_size
  timeout       = var.lambda_timeout
  
  environment {
    variables = {
      MODEL_BUCKET    = aws_s3_bucket.model_storage.id
      MODEL_KEY       = "models/best_model.pt"
      DYNAMODB_TABLE  = aws_dynamodb_table.predictions.name
    }
  }
  
  # Skip for now - will add actual deployment package later
  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}
