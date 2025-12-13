import pytest
import torch
from unittest.mock import MagicMock
from src.models.predictor import ToxicityPredictor

class TestToxicityPredictor:
    @pytest.fixture
    def mock_model(self):
        model = MagicMock()
        # Mock output logits
        model.return_value.logits = torch.tensor([[0.8, -0.5, 0.9, -1.0, 0.2, -0.8]])
        return model

    @pytest.fixture
    def mock_tokenizer(self):
        tokenizer = MagicMock()
        tokenizer.encode_plus.return_value = {
            'input_ids': torch.tensor([[1, 2, 3]]),
            'attention_mask': torch.tensor([[1, 1, 1]])
        }
        return tokenizer

    @pytest.fixture
    def predictor(self, mock_model, mock_tokenizer):
        return ToxicityPredictor(mock_model, mock_tokenizer)

    def test_predict_structure(self, predictor):
        """Test the structure of the prediction output."""
        result = predictor.predict("test text")
        
        assert "is_toxic" in result
        assert "toxicity_scores" in result
        assert "flagged_categories" in result
        assert "confidence" in result
        
        # Check scores match labels
        assert set(result["toxicity_scores"].keys()) == set(ToxicityPredictor.LABEL_COLUMNS)

    def test_threshold_logic(self, predictor, mock_model):
        """Test that threshold correctly identifies toxic content."""
        # Logits: 0.8 (sigmoid -> ~0.69) -> Toxic
        #        -0.5 (sigmoid -> ~0.37) -> Safe
        #         0.9 (sigmoid -> ~0.71) -> Toxic
        
        result = predictor.predict("test")
        
        assert result["is_toxic"] is True
        assert "toxic" in result["flagged_categories"]
        assert "obscene" in result["flagged_categories"] # 3rd label
        assert "severe_toxic" not in result["flagged_categories"] # 2nd label

    def test_safe_content(self, predictor, mock_model):
        """Test with all low logits."""
        # Set all logits to negative values (low probability)
        mock_model.return_value.logits = torch.tensor([[-2.0] * 6])
        
        result = predictor.predict("safe text")
        assert result["is_toxic"] is False
        assert len(result["flagged_categories"]) == 0

    def test_predict_batch(self, predictor):
        """Test batch prediction."""
        results = predictor.predict_batch(["text1", "text2"])
        assert len(results) == 2
        assert results[0]["is_toxic"] is True # Based on default mock
