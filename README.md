# 🛡️ Real-Time Content Moderation System

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An intelligent NLP-powered content moderation system that automatically detects and flags toxic content in real-time using state-of-the-art transformer models and serverless cloud architecture.

---

## 📋 Problem Statement

Online platforms face a critical challenge: **millions of user-generated comments are posted daily**, making manual moderation impossible to scale. Toxic content—including harassment, hate speech, and threats—damages user experience, creates legal liability, and drives users away from platforms.

**Traditional solutions fall short:**
- Manual moderation is slow, expensive, and doesn't scale
- Simple keyword filtering misses context and generates false positives
- Delayed moderation allows harmful content to spread

**This system provides:**
- Real-time automated detection of toxic content
- Context-aware classification using deep learning
- Scalable serverless architecture that handles traffic spikes
- Cost-efficient pay-per-use model suitable for platforms of any size

---

## ✨ Key Features

- **Multi-Category Toxicity Detection**: Identifies toxic, obscene, threatening, insulting, and hate speech content
- **Real-Time Processing**: Sub-second inference time using serverless architecture
- **Transformer-Based NLP**: Leverages pre-trained BERT models fine-tuned on toxicity datasets
- **RESTful API**: Easy integration with existing platforms via FastAPI
- **Automated Logging**: Tracks all predictions in DynamoDB for monitoring and improvement
- **Cloud-Native**: Built on AWS serverless infrastructure (Lambda, S3, DynamoDB)
- **Scalable**: Auto-scales to handle thousands of concurrent requests

---

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   FastAPI       │
│  (API Gateway)  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐         ┌──────────────┐
│  AWS Lambda     │────────▶│  Amazon S3   │
│  (Inference)    │         │ (Model Store)│
└──────┬──────────┘         └──────────────┘
       │
       │ Load Model
       ▼
┌─────────────────┐
│  Transformers   │
│   (DistilBERT)  │
└──────┬──────────┘
       │
       │ Predict
       ▼
┌─────────────────┐
│   DynamoDB      │
│  (Logging &     │
│   Results)      │
└─────────────────┘
```

**Flow:**
1. User sends text via API request
2. FastAPI receives and validates input
3. AWS Lambda loads model from S3
4. Transformer model performs inference
5. Prediction logged to DynamoDB
6. Result returned to user (toxic/clean + confidence scores)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Core programming language for ML and API development |
| **Transformers (Hugging Face)** | Access to pre-trained NLP models (DistilBERT) for transfer learning |
| **FastAPI** | High-performance API framework with automatic documentation |
| **AWS Lambda** | Serverless compute for cost-efficient, auto-scaling inference |
| **Amazon S3** | Cloud storage for datasets, trained models, and artifacts |
| **Amazon DynamoDB** | NoSQL database for logging predictions and monitoring |
| **PyTorch** | Deep learning framework for model training and inference |
| **Pandas & NumPy** | Data manipulation and preprocessing |
| **Scikit-learn** | Model evaluation metrics and utilities |

---

## 📊 Dataset

**Primary Dataset**: [Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge)

- **Size**: 159,571 Wikipedia comments
- **Labels**: Multi-label classification across 6 categories
  - Toxic
  - Severe Toxic
  - Obscene
  - Threat
  - Insult
  - Identity Hate
- **Challenge**: Highly imbalanced dataset with only ~10% toxic samples

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- AWS Account (Free Tier eligible)
- Git

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/content-moderation-system.git
cd content-moderation-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download dataset**
- Visit [Kaggle Competition](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data)
- Download `train.csv`, `test.csv`, `test_labels.csv`
- Place in `data/` folder

5. **Run exploratory data analysis**
```bash
jupyter notebook notebooks/01_eda_toxic_comments.ipynb
```

### AWS Setup (Coming Soon)
Instructions for deploying to AWS Lambda will be added after local development is complete.

---

## 💻 Usage

### API Example (After Deployment)

**Endpoint**: `POST /moderate`

**Request**:
```json
{
  "text": "Your comment text here"
}
```

**Response**:
```json
{
  "text": "Your comment text here",
  "predictions": {
    "toxic": 0.92,
    "severe_toxic": 0.15,
    "obscene": 0.78,
    "threat": 0.05,
    "insult": 0.65,
    "identity_hate": 0.12
  },
  "is_toxic": true,
  "timestamp": "2025-12-06T10:30:00Z"
}
```

---

## 📈 Project Status

### ✅ Completed
- [x] Project initialization and repository setup
- [x] Folder structure and version control

### 🚧 In Progress
- [ ] Exploratory Data Analysis (EDA)
- [ ] Data preprocessing pipeline
- [ ] Model selection and fine-tuning
- [ ] FastAPI development
- [ ] AWS Lambda deployment
- [ ] DynamoDB integration
- [ ] Testing and evaluation

### 🔮 Future Enhancements
- [ ] Multi-language support
- [ ] Real-time dashboard for monitoring
- [ ] A/B testing framework for model versions
- [ ] User feedback loop for model improvement
- [ ] Explainability features (highlight toxic phrases)
- [ ] Rate limiting and authentication
- [ ] Model versioning and rollback capability

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Your Name**
- GitHub: (https://github.com/Arv-ind-s)
- LinkedIn: [(https://www.linkedin.com/in/97aravind-s/)
- Email: arvindsathyan@gmail.com

---

## 🙏 Acknowledgments

- Jigsaw/Conversation AI for the toxic comment dataset
- Hugging Face for transformer models and libraries
- AWS for cloud infrastructure

---

**⭐ If you find this project helpful, please consider giving it a star!**
