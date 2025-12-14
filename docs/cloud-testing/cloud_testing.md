# Cloud Testing Results

## Setup
- **Model**: DistilBERT fine-tuned (268MB)
- **Environment**: AWS Lambda (3008MB Memory, 300s Timeout) + API Gateway
- **Storage**: S3 Bucket (Model loaded from S3)
- **Date**: December 14, 2025

## Test Results

### 1. Health Check
- **Endpoint**: `https://2a104jsmyk.execute-api.us-east-1.amazonaws.com/health`
- **Result**: `{"status":"healthy","model_loaded":true,"version":"1.0.0"}`
- ✅ API is reachable and model is loaded.

### 2. Toxic Comment Test
**Endpoint**: `POST /moderate`

**Input Payload**:
```json
{
  "text": "You are stupid and I hate you."
}
```

**Response**:
```json
{
  "text": "You are stupid and I hate you.",
  "is_toxic": true,
  "toxicity_scores": {
    "toxic": 0.997,
    "severe_toxic": 0.157,
    "obscene": 0.908,
    "threat": 0.086,
    "insult": 0.995,
    "identity_hate": 0.064
  },
  "flagged_categories": [
    "toxic",
    "obscene",
    "insult"
  ],
  "confidence": 0.997,
  "timestamp": "2025-12-14T09:03:57.050405"
}
```

### 3. Performance
- **Cold Start**: ~60s (Initial model download from S3 + Load)
- **Warm Start**: ~2.54s (Inference time)
- **Status**: Acceptable for initial deployment.

## Conclusion
✅ Cloud infrastructure is fully functional.
✅ S3 Integration works correctly (Model download validated).
✅ Inference matches local model performance.
✅ Deployment successful using Docker + Terraform.

## Screenshots
*(Add screenshots of AWS Console, CloudWatch Logs, and Postman tests here)*
- [Screenshots Directory](screenshots/)
