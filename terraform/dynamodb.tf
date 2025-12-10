resource "aws_dynamodb_table" "predictions" {
  name         = "${var.dynamodb_table_name}-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"  # Free Tier: 25 write units, 25 read units
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
  
  # TTL to auto-delete old predictions (cost control)
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  # EXPLICITLY DISABLE point-in-time recovery (costs money)
  point_in_time_recovery {
    enabled = false
  }
  
  tags = {
    Name       = "Moderation Predictions"
    CostCenter = "Free Tier"
  }
}
