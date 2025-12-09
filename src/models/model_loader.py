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
        self.fine_tuned_loaded = False  # Track if fine-tuned weights were loaded
        
    def load_model(self):
        """Load model and tokenizer."""
        try:
            logger.info(f"Loading tokenizer: {self.model_name}")
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
            
            logger.info(f"Loading base model: {self.model_name}")
            self.model = DistilBertForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=6,
                problem_type="multi_label_classification"
            )
            
            # Load fine-tuned weights if available
            if self.model_path:
                model_path_obj = Path(self.model_path)
                
                if model_path_obj.exists():
                    logger.info(f"📦 Fine-tuned model file found at: {self.model_path}")
                    logger.info(f"📦 File size: {model_path_obj.stat().st_size / (1024*1024):.2f} MB")
                    
                    try:
                        # Load the state dict
                        state_dict = torch.load(self.model_path, map_location=self.device)
                        
                        # Load into model
                        self.model.load_state_dict(state_dict)
                        self.fine_tuned_loaded = True
                        
                        logger.info("✅ Fine-tuned weights loaded successfully!")
                        logger.info("✅ Using YOUR trained model (not base DistilBERT)")
                        
                    except Exception as e:
                        logger.error(f"❌ Error loading fine-tuned weights: {str(e)}")
                        logger.warning("⚠️  Falling back to base DistilBERT model")
                        self.fine_tuned_loaded = False
                else:
                    logger.warning(f"⚠️  Model file not found at: {self.model_path}")
                    logger.warning(f"⚠️  Current working directory: {os.getcwd()}")
                    logger.warning(f"⚠️  Using base DistilBERT model (NOT your fine-tuned model)")
                    self.fine_tuned_loaded = False
            else:
                logger.warning("⚠️  No model_path provided. Using base DistilBERT model.")
                self.fine_tuned_loaded = False
            
            # Move to device and set to eval mode
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model configuration:")
            logger.info(f"  - Device: {self.device}")
            logger.info(f"  - Fine-tuned: {self.fine_tuned_loaded}")
            logger.info(f"  - Num labels: 6")
            
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