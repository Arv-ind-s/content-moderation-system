"""
Model loading and initialization.
Handles downloading from S3 (production) or loading locally (development).
"""

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)


class ModelLoader:
    """Handles model loading and caching."""
    
    def __init__(
        self, 
        model_name: str = "distilbert-base-uncased",
        model_path: str = None,
        device: str = None
    ):
        """
        Initialize model loader.
        
        Args:
            model_name: Hugging Face model name
            model_path: Path to fine-tuned model weights
            device: Device to load model on (cuda/cpu)
        """
        self.model_name = model_name
        self.model_path = model_path
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """Load model and tokenizer."""
        try:
            logger.info(f"Loading tokenizer: {self.model_name}")
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
            
            logger.info(f"Loading model: {self.model_name}")
            self.model = DistilBertForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=6,
                problem_type="multi_label_classification"
            )
            
            # Load fine-tuned weights if available
            if self.model_path and Path(self.model_path).exists():
                logger.info(f"Loading fine-tuned weights from: {self.model_path}")
                state_dict = torch.load(self.model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                logger.info("Fine-tuned weights loaded successfully")
            else:
                logger.warning(f"Model path not found: {self.model_path}. Using base model.")
            
            # Move to device and set to eval mode
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None and self.tokenizer is not None
    
    def get_model(self):
        """Get the loaded model."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded. Call load_model() first.")
        return self.model
    
    def get_tokenizer(self):
        """Get the loaded tokenizer."""
        if not self.is_loaded():
            raise RuntimeError("Tokenizer not loaded. Call load_model() first.")
        return self.tokenizer