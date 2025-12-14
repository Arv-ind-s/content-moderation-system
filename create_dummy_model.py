
import os
import torch
from transformers import DistilBertForSequenceClassification

# Ensure directory exists
os.makedirs("src/models", exist_ok=True)

print("Downloading base model...")
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=6,
    problem_type="multi_label_classification"
)

output_path = "src/models/best_model.pt"
print(f"Saving model to {output_path}...")
torch.save(model.state_dict(), output_path)
print("✅ Model saved successfully")
