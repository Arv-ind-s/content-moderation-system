# Infrastructure as Code - Terraform

## Overview
Terraform configuration for deploying the Content Moderation System to AWS.

## Architecture
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│  AWS Lambda     │─────▶│  Amazon S3   │
│  (Inference)    │      │ (Model Store)│
└──────┬──────────┘      └──────────────┘
       │
       ▼
┌─────────────────┐
│   DynamoDB      │
│ (Predictions)   │
└─────────────────┘
```

## Resources Provisioned

1. **S3 Bucket** - Stores trained model artifacts
2. **Lambda Function** - Runs model inference
3. **DynamoDB Table** - Logs predictions and metrics
4. **IAM Roles** - Permissions for Lambda
5. **CloudWatch Logs** - Monitoring and debugging

## Prerequisites

- AWS Account
- AWS CLI configured (`aws configure`)
- Terraform >= 1.0 installed

## Quick Start
```bash
# Initialize Terraform
terraform init

# Preview infrastructure changes
terraform plan

# Deploy
terraform apply

# Destroy (cleanup)
terraform destroy
```

## Configuration

Edit `variables.tf` to customize:
- AWS region
- Lambda memory/timeout
- Resource names

## Outputs

After `terraform apply`, you'll get:
- S3 bucket name
- Lambda function ARN
- DynamoDB table name
- API endpoint (if enabled)

## Cost Estimate

With AWS Free Tier:
- S3: ~$1/month
- Lambda: ~$2/month  
- DynamoDB: ~$1/month
- **Total**: ~$4-5/month

## Status

✅ Terraform directory and structure created

