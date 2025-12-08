"""
Model inference and prediction logic.
"""

import torch
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class ToxicityPredictor:
    """Handles model inference for toxicity prediction."""
    
    LABEL_COLUMNS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    THRESHOLD = 0.5  # Probability threshold for binary classification
    
    def __init__(self, model, tokenizer, max_length: int = 256, device: str = "cpu"):
        """
        Initialize predictor.
        
        Args:
            model: Loaded DistilBERT model
            tokenizer: Loaded tokenizer
            max_length: Maximum sequence length
            device: Device for inference
        """
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.device = device
        
    def predict(self, text: str) -> Dict:
        """
        Predict toxicity for given text.
        
        Args:
            text: Preprocessed text
            
        Returns:
            Dictionary with predictions
        """
        try:
            # Tokenize
            encoded = self.tokenizer.encode_plus(
                text,
                add_special_tokens=True,
                max_length=self.max_length,
                padding='max_length',
                truncation=True,
                return_attention_mask=True,
                return_tensors='pt'
            )
            
            # Move to device
            input_ids = encoded['input_ids'].to(self.device)
            attention_mask = encoded['attention_mask'].to(self.device)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
                logits = outputs.logits
                
                # Apply sigmoid to get probabilities
                probabilities = torch.sigmoid(logits)
                probs = probabilities.cpu().numpy()[0]
            
            # Create results dictionary
            toxicity_scores = {
                label: float(prob) 
                for label, prob in zip(self.LABEL_COLUMNS, probs)
            }
            
            # Determine if toxic (any category above threshold)
            is_toxic = any(prob > self.THRESHOLD for prob in probs)
            
            # Get flagged categories
            flagged_categories = [
                label for label, prob in toxicity_scores.items() 
                if prob > self.THRESHOLD
            ]
            
            # Calculate overall confidence (max probability)
            confidence = float(np.max(probs))
            
            return {
                'is_toxic': is_toxic,
                'toxicity_scores': toxicity_scores,
                'flagged_categories': flagged_categories,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise
    
    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """
        Predict toxicity for multiple texts.
        
        Args:
            texts: List of preprocessed texts
            
        Returns:
            List of prediction dictionaries
        """
        return [self.predict(text) for text in texts]