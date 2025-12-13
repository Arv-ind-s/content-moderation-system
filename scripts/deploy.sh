#!/bin/bash
set -e

# Configuration
AWS_REGION="us-east-1"
ECR_REPO_NAME="content-moderation-repo-dev"  # Matches terraform naming convention
LAMBDA_FUNCTION_NAME="content-moderation-api-dev"

# Get Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_URI="${ECR_URI}/${ECR_REPO_NAME}:latest"

echo "🚀 Starting deployment..."
echo "   Region: ${AWS_REGION}"
echo "   Account: ${ACCOUNT_ID}"
echo "   Image: ${IMAGE_URI}"

# Login to ECR
echo "🔑 Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URI}

# Build Image
echo "📦 Building Docker image..."
# Build from project root
docker build -t ${ECR_REPO_NAME} -f Dockerfile .

# Tag Image
echo "🏷️ Tagging image..."
docker tag ${ECR_REPO_NAME}:latest ${IMAGE_URI}

# Push Image
echo "⬆️ Pushing to ECR..."
docker push ${IMAGE_URI}

# Update Lambda
echo "🔄 Updating Lambda function..."
aws lambda update-function-code \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --image-uri ${IMAGE_URI} \
    --region ${AWS_REGION}

echo "✅ Deployment complete!"
