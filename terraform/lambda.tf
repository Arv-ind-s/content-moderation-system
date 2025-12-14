resource "aws_lambda_function" "moderation_api" {
  function_name = "${var.project_name}-api-${var.environment}"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.moderation_repo.repository_url}:latest"
  
  memory_size   = 3008
  timeout       = 300
  architectures = ["x86_64"]
  
  environment {
    variables = {
      MODEL_BUCKET    = aws_s3_bucket.model_storage.id
      MODEL_KEY       = "models/best_model.pt"
      MODEL_PATH      = "/tmp/best_model.pt"
      DYNAMODB_TABLE  = aws_dynamodb_table.predictions.name
      TRANSFORMERS_CACHE = "/tmp/transformers_cache"
      HF_HOME            = "/tmp/hf_home"
    }
  }
  
  depends_on = [aws_cloudwatch_log_group.lambda_logs]
  
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
