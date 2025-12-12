resource "aws_lambda_function" "moderation_api" {
  filename      = "lambda_function.zip"
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
  
  depends_on = [aws_cloudwatch_log_group.lambda_logs]
  
  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
  
  tags = {
    CostCenter = "Free Tier"
  }
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.project_name}-api-${var.environment}"
  retention_in_days = 7
  
  tags = {
    Name       = "Lambda Logs"
    CostCenter = "Free Tier"
  }
}
