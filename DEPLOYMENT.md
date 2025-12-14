# ☁️ Comprehensive Cloud Deployment Guide

This document provides a complete, step-by-step walkthrough to deploy the Content Moderation System to AWS. It covers everything from cloning the repository to tearing down the infrastructure.

---

## ✅ Prerequisites

Before starting, ensure you have the following installed:

1.  **AWS CLI**: [Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (Run `aws configure` to set credentials)
2.  **Terraform**: [Install Guide](https://developer.hashicorp.com/terraform/install) (v1.0+)
3.  **Docker**: [Install Guide](https://docs.docker.com/get-docker/) (Must be running)
4.  **Python 3.11** & **Git**

---

## 🚀 Step 1: Clone & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Arv-ind-s/content-moderation-system.git
    cd content-moderation-system
    ```

2.  **Set up Virtual Environment**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

---

## 🏗️ Step 2: Infrastructure Provisioning

We use **Terraform** to create the AWS resources (S3, ECR, Lambda, DynamoDB, API Gateway).

1.  **Initialize Terraform**
    ```bash
    cd terraform
    terraform init
    ```

2.  **Create Repositories & Buckets**
    (We apply in stages to ensure the Docker image repository exists before the Lambda tries to pull from it)
    ```bash
    # Create ECR Repo and S3 Bucket first
    terraform apply -target=aws_ecr_repository.moderation_repo -target=aws_s3_bucket.model_storage -auto-approve
    ```
    
    *Note: The output will display your ECR Repo URL and S3 Bucket Name.*

---

## 📦 Step 3: Model Upload

The system requires your fine-tuned model to be present in the S3 bucket.

1.  **Run the Upload Script**
    (This automatically finds the created S3 bucket and uploads `models/best_model.pt`)
    ```bash
    # From project root
    cd ..
    python scripts/upload_model.py
    ```

---

## 🐳 Step 4: Build & Deploy Application

Now we build the Docker image and deploy the Lambda function.

1.  **Make Deploy Script Executable**
    ```bash
    chmod +x scripts/deploy.sh
    ```

2.  **Run Deployment**
    ```bash
    ./scripts/deploy.sh
    ```
    *This will build the Docker image (amd64), push it to ECR, and update the Lambda function.*

3.  **Finalize Infrastructure**
    (Now that the image is in ECR, we create the Lambda and API Gateway)
    ```bash
    cd terraform
    terraform apply -auto-approve
    ```

    **Copy the `api_endpoint` from the output!**  
    Example: `https://xyz123.execute-api.us-east-1.amazonaws.com/`

---

## 🧪 Step 5: Cloud Testing

Verify the deployment works directly on AWS.

1.  **Health Check**
    ```bash
    curl https://<YOUR_API_ID>.execute-api.us-east-1.amazonaws.com/health
    ```
    *Expected: `{"status":"healthy", ...}`*

2.  **Test Toxicity Detection**
    You can use the provided verification script:
    ```bash
    # Update the URL in the script first if needed, or just run curl:
    curl -X POST "https://<YOUR_API_ID>.execute-api.us-east-1.amazonaws.com/moderate" \
         -H "Content-Type: application/json" \
         -d '{"text": "You are stupid and I hate you."}'
    ```

---

## 🧹 Step 6: Cleanup (Destroy)

**CRITICAL**: Destroy resources to avoid AWS costs.

1.  **Destroy Everything**
    ```bash
    cd terraform
    terraform destroy -auto-approve
    ```
    
    *Note: We have configured S3 and ECR with `force_destroy=true`, so this command will automatically delete all images and model files for you.*

---
