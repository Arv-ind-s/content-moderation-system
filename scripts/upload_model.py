
import boto3
import os
import sys
from pathlib import Path
from botocore.exceptions import ClientError, NoCredentialsError

def get_model_bucket():
    """
    Finds the model bucket created by Terraform.
    Assumes naming convention: *-model-storage-*
    """
    s3 = boto3.client('s3')
    try:
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            if 'content-moderation-models' in bucket['Name']:
                return bucket['Name']
    except ClientError as e:
        print(f"❌ Error listing buckets: {e}")
        return None
    except NoCredentialsError:
        print("❌ No AWS credentials found. Please configure AWS CLI.")
        return None
    return None

def upload_model():
    # 1. Locate Model File
    project_root = Path(__file__).parent.parent
    model_path = project_root / "models" / "best_model.pt"
    
    if not model_path.exists():
        print(f"❌ Model file not found at: {model_path}")
        print("   Please ensure you have trained the model and it is saved at this location.")
        sys.exit(1)
        
    print(f"✅ Found model file: {model_path}")
    file_size_mb = model_path.stat().st_size / (1024 * 1024)
    print(f"   Size: {file_size_mb:.2f} MB")

    # 2. Identify S3 Bucket
    print("🔍 Looking for S3 bucket...")
    bucket_name = get_model_bucket()
    
    if not bucket_name:
        print("❌ Could not find model storage bucket.")
        print("   Ensure Terraform has been applied successfully.")
        sys.exit(1)
    
    print(f"✅ Found bucket: {bucket_name}")

    # 3. Upload to S3
    s3_key = "models/best_model.pt"
    s3 = boto3.client('s3')
    
    print(f"🚀 Uploading to s3://{bucket_name}/{s3_key}...")
    
    try:
        s3.upload_file(
            str(model_path), 
            bucket_name, 
            s3_key,
            ExtraArgs={'ContentType': 'application/octet-stream'}
        )
        print("✅ Upload successful!")
        print("   The Lambda function will now download this model on startup.")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    upload_model()
