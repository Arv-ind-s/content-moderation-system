import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app

# Mock data
MOCK_PREDICTION_TOXIC = {
    'is_toxic': True,
    'toxicity_scores': {'toxic': 0.95, 'severe_toxic': 0.1, 'obscene': 0.8, 'threat': 0.0, 'insult': 0.7, 'identity_hate': 0.0},
    'flagged_categories': ['toxic', 'obscene', 'insult'],
    'confidence': 0.95
}

MOCK_PREDICTION_CLEAN = {
    'is_toxic': False,
    'toxicity_scores': {'toxic': 0.01, 'severe_toxic': 0.0, 'obscene': 0.0, 'threat': 0.0, 'insult': 0.0, 'identity_hate': 0.0},
    'flagged_categories': [],
    'confidence': 0.99
}

@pytest.fixture
def client():
    # Mock the predictor and model_loader to avoid loading actual model
    with patch('src.api.main.predictor') as mock_pred, \
         patch('src.api.main.model_loader') as mock_loader:
        
        # Setup mock return values
        mock_pred.predict.return_value = MOCK_PREDICTION_TOXIC
        mock_loader.is_loaded.return_value = True
        mock_loader.fine_tuned_loaded = True
        
        with TestClient(app) as c:
            yield c

class TestAPIEndpoints:
    def test_root(self, client):
        """Test root endpoint returns version info."""
        response = client.get("/")
        assert response.status_code == 200
        assert "version" in response.json()
        assert "status" in response.json()

    def test_health_check(self, client):
        """Test health endpoint returns correct status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["model_loaded"] is True

    @pytest.mark.parametrize("payload, expected_status, error_match", [
        ({"text": ""}, 400, "empty"),
        ({"text": "   "}, 400, "empty"),
        ({}, 422, "field required"), # Missing field
        ({"text": "a" * 6000}, 400, "exceeds maximum length"),
    ])
    def test_moderate_validation_errors(self, client, payload, expected_status, error_match):
        """Test input validation for moderation endpoint."""
        response = client.post("/moderate", json=payload)
        assert response.status_code == expected_status
        if error_match:
            # 422 errors have a different structure
            if expected_status == 422:
                assert response.json()["detail"][0]["msg"]
            else:
                assert error_match in response.json()["detail"].lower()

    def test_moderate_success_toxic(self, client):
        """Test successful moderation of toxic text."""
        response = client.post("/moderate", json={"text": "You are terrible"})
        assert response.status_code == 200
        data = response.json()
        assert data["is_toxic"] is True
        assert "toxic" in data["flagged_categories"]

    def test_moderate_success_clean(self, client):
        """Test successful moderation of clean text."""
        # Update mock for this specific test
        with patch('src.api.main.predictor.predict', return_value=MOCK_PREDICTION_CLEAN):
            response = client.post("/moderate", json={"text": "Hello world"})
            assert response.status_code == 200
            data = response.json()
            assert data["is_toxic"] is False
            assert len(data["flagged_categories"]) == 0

    def test_service_unavailable(self):
        """Test 503 when model is not loaded."""
        # Create a client where model_loader.is_loaded returns False
        with patch('src.api.main.model_loader') as mock_loader:
            mock_loader.is_loaded.return_value = False
            with TestClient(app) as c:
                response = c.post("/moderate", json={"text": "test"})
                assert response.status_code == 503
                assert "model not loaded" in response.json()["detail"].lower()

    def test_internal_server_error(self, client):
        """Test 500 handling when prediction fails."""
        with patch('src.api.main.predictor.predict', side_effect=Exception("Model Crash")):
            response = client.post("/moderate", json={"text": "crash me"})
            assert response.status_code == 500
            assert "internal server error" in response.json()["detail"].lower()
