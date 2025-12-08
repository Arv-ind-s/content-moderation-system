from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime


class ModerationRequest(BaseModel):
    """Request model for content moderation."""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to moderate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a sample comment to moderate"
            }
        }


class ToxicityScores(BaseModel):
    """Toxicity scores for all categories."""
    toxic: float = Field(..., ge=0.0, le=1.0)
    severe_toxic: float = Field(..., ge=0.0, le=1.0)
    obscene: float = Field(..., ge=0.0, le=1.0)
    threat: float = Field(..., ge=0.0, le=1.0)
    insult: float = Field(..., ge=0.0, le=1.0)
    identity_hate: float = Field(..., ge=0.0, le=1.0)


class ModerationResponse(BaseModel):
    """Response model for content moderation."""
    text: str
    is_toxic: bool
    toxicity_scores: ToxicityScores
    flagged_categories: List[str]
    confidence: float
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a sample comment",
                "is_toxic": False,
                "toxicity_scores": {
                    "toxic": 0.12,
                    "severe_toxic": 0.03,
                    "obscene": 0.05,
                    "threat": 0.01,
                    "insult": 0.08,
                    "identity_hate": 0.02
                },
                "flagged_categories": [],
                "confidence": 0.88,
                "timestamp": "2025-12-06T10:30:00"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    version: str