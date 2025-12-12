resource "aws_dynamodb_table" "predictions" {
  name         = "${var.dynamodb_table_name}-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "prediction_id"
  range_key    = "timestamp"
  
  attribute {
    name = "prediction_id"
    type = "S"
  }
  
  attribute {
    name = "timestamp"
    type = "N"
  }
  
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  point_in_time_recovery {
    enabled = false
  }
  
  tags = {
    Name       = "Moderation Predictions"
    CostCenter = "Free Tier"
  }
}
