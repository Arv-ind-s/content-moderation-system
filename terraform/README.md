# Infrastructure as Code - Terraform

## Overview
Terraform configuration for deploying the Content Moderation System to AWS using a **serverless Docker container** architecture.

## Architecture
```
┌─────────────┐
│   Client    │
│  (HTTP/1.1) │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
│   (HTTP API)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│  AWS Lambda     │◀─────│     ECR      │
│ (Docker Image)  │      │(Image Repo)  │
└──────┬──────────┘      └──────────────┘
       │
       │ Load Model
       ▼
┌─────────────────┐      ┌──────────────┐
│   Amazon S3     │      │   DynamoDB   │
│ (Model Storage) │      │ (Predictions)│
└─────────────────┘      └──────────────┘
```

## Resources Provisioned

1.  **ECR Repository** - Stores the Docker image for the Lambda function.
2.  **Lambda Function** - Runs the FastAPI application (packaged as a Docker container).
3.  **API Gateway (HTTP API)** - Provides a public HTTP endpoint for the Lambda.
4.  **S3 Bucket** - Stores the trained model artifacts (downloaded by Lambda on startup).
5.  **DynamoDB Table** - Logs predictions and metrics (On-Demand capacity).
6.  **IAM Roles** - Permissions for Lambda to access S3, DynamoDB, and CloudWatch.
7.  **CloudWatch Logs** - Monitoring and debugging.

## 🚀 Deployment

> [!IMPORTANT]
> **Deployment is a multi-step process** because the Lambda function requires the Docker image to exist before it can be created.

Please refer to the main **[Deployment Guide](../DEPLOYMENT.md)** for detailed instructions.

### Quick Summary
1.  **Create Repo**: `terraform apply -target=aws_ecr_repository.moderation_repo`
2.  **Push Image**: `../scripts/deploy.sh`
3.  **Deploy All**: `terraform apply`

## Configuration

Edit `variables.tf` to customize:
-   `aws_region`: Deployment region (default: `us-east-1`)
-   `lambda_memory_size`: RAM for Lambda (default: `512`)
-   `lambda_timeout`: Timeout in seconds (default: `30`)

## Outputs

After `terraform apply`, you will receive:
-   `api_endpoint`: The public URL to access your API.
-   `ecr_repository_url`: The URL of your private Docker registry.
-   `s3_bucket_name`: Bucket for model storage.

## Cost Estimate (Optimized)

This infrastructure is optimized for the **AWS Free Tier** and low-cost operation:

*   **API Gateway (HTTP API)**: ~$1.00 per million requests (Free Tier: 1M/month for 12 months).
*   **Lambda (ARM64)**: Pay per millisecond of execution.
*   **DynamoDB**: Pay-per-request (On-Demand). $0 idle cost.
*   **ECR**: Storage costs for the Docker image (~$0.10/GB/month).
*   **S3**: Storage costs for the model file (~$0.023/GB/month).

**Total Idle Cost**: < $0.50 / month (mostly storage).
