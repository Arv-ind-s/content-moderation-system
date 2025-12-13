import pytest
import os
from unittest.mock import MagicMock, patch
from src.models.model_loader import ModelLoader

class TestModelLoader:
    @pytest.fixture
    def loader(self):
        return ModelLoader(model_path="models/test_model.pt")

    @patch("src.models.model_loader.DistilBertTokenizer.from_pretrained")
    @patch("src.models.model_loader.DistilBertForSequenceClassification.from_pretrained")
    def test_load_base_model(self, mock_model, mock_tokenizer, loader):
        """Test loading the base model without fine-tuned weights."""
        # Setup mocks
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()
        
        # Ensure model path doesn't exist so it skips fine-tuning load
        with patch("pathlib.Path.exists", return_value=False):
            loader.load_model()
        
        assert loader.is_loaded()
        assert loader.fine_tuned_loaded is False
        mock_tokenizer.assert_called_once()
        mock_model.assert_called_once()

    @patch("src.models.model_loader.boto3.client")
    def test_download_from_s3(self, mock_boto, loader):
        """Test S3 download logic."""
        # Setup env vars
        with patch.dict(os.environ, {"MODEL_BUCKET": "test-bucket", "MODEL_KEY": "model.pt"}):
            # Mock S3 client
            mock_s3 = MagicMock()
            mock_boto.return_value = mock_s3
            
            # Run download
            loader._download_from_s3()
            
            # Verify call
            mock_s3.download_file.assert_called_with(
                "test-bucket", 
                "model.pt", 
                "models/test_model.pt"
            )

    @patch("src.models.model_loader.boto3.client")
    def test_download_s3_failure(self, mock_boto, loader):
        """Test graceful handling of S3 failure."""
        with patch.dict(os.environ, {"MODEL_BUCKET": "test-bucket"}):
            mock_s3 = MagicMock()
            mock_boto.return_value = mock_s3
            mock_s3.download_file.side_effect = Exception("S3 Error")
            
            # Should log error but not crash
            loader._download_from_s3()

    def test_get_model_not_loaded(self, loader):
        """Test error when accessing model before loading."""
        with pytest.raises(RuntimeError):
            loader.get_model()
