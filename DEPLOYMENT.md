# 🚀 Deployment Guide

This guide details how to deploy the Content Moderation System to AWS.
Because we use **Docker containers** for Lambda (to handle large dependencies like PyTorch), the deployment process involves a few specific steps.

## ✅ Prerequisites

1.  **AWS CLI**: Installed and configured with `aws configure`.
2.  **Terraform**: Installed (v1.0+).
3.  **Docker**: Installed and running.
4.  **Python 3.11**: For local development (optional).

---

## 🛠️ Deployment Steps

### 1. Initialize Terraform
Navigate to the terraform directory and initialize the project.

```bash
cd terraform
terraform init
```

### 2. Create ECR Repository
Before we can deploy the Lambda function, we need a place to store its Docker image. We must create the ECR repository first.

```bash
# Create only the ECR repository
terraform apply -target=aws_ecr_repository.moderation_repo
```

Type `yes` to confirm.

### 3. Build and Push Docker Image
Now that the repository exists, we can build our Docker image and push it to AWS. We have a script to automate this.

```bash
# Go back to root directory
cd ..

# Make script executable (first time only)
chmod +x scripts/deploy.sh

# Run deployment script
./scripts/deploy.sh
```

**What this script does:**
1.  Logs into AWS ECR via Docker.
2.  Builds the Docker image from the `Dockerfile`.
3.  Pushes the image to your ECR repository.
4.  Updates the Lambda function code (if it already exists).

### 4. Deploy Infrastructure
Now that the image is in ECR, we can deploy the rest of the infrastructure (Lambda, API Gateway, DynamoDB, S3).

```bash
cd terraform
terraform apply
```

Type `yes` to confirm.

---

## 🧪 Testing the Deployment

### 1. Get the API Endpoint
After `terraform apply` finishes, it will output the `api_endpoint`. It looks like this:
`https://<random-id>.execute-api.us-east-1.amazonaws.com`

### 2. Send a Request
You can use `curl` or Postman.

```bash
curl -X POST "https://<your-api-endpoint>/moderate" \
     -H "Content-Type: application/json" \
     -d '{"text": "This is a test comment."}'
```

---

## 🧹 Cleanup (Destroy Resources)
To avoid incurring costs when you are done testing:

1.  **Destroy Infrastructure**:
    ```bash
    cd terraform
    terraform destroy
    ```

2.  **Delete ECR Images** (Terraform might fail to delete a non-empty repo):
    *   Go to AWS Console > ECR.
    *   Select your repository.
    *   Delete all images.
    *   Run `terraform destroy` again if needed.
