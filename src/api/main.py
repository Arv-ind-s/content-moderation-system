"""
FastAPI application for content moderation.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

from src.api.schemas import ModerationRequest, ModerationResponse, HealthResponse, ToxicityScores
from src.models.model_loader import ModelLoader
from src.models.predictor import ToxicityPredictor
from src.utils.text_processing import clean_text, validate_text

# Get the project root directory (where .env is located)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load environment variables from project root
env_path = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log environment variables (for debugging)
logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
logger.info(f"Loading .env from: {env_path}")
logger.info(f"MODEL_NAME from env: {os.getenv('MODEL_NAME')}")
logger.info(f"MODEL_PATH from env: {os.getenv('MODEL_PATH')}")

# Global variables for model
model_loader = None
predictor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Load model
    global model_loader, predictor
    
    logger.info("Starting up: Loading model...")
    
    model_name = os.getenv("MODEL_NAME", "distilbert-base-uncased")
    model_path_relative = os.getenv("MODEL_PATH", "models/best_model.pt")
    max_length = int(os.getenv("MAX_LENGTH", "256"))
    
    # Resolve absolute path for model
    model_path_absolute = PROJECT_ROOT / model_path_relative
    
    logger.info(f"Model configuration:")
    logger.info(f"  - Model name: {model_name}")
    logger.info(f"  - Model path (relative): {model_path_relative}")
    logger.info(f"  - Model path (absolute): {model_path_absolute}")
    logger.info(f"  - Model file exists: {model_path_absolute.exists()}")
    logger.info(f"  - Max length: {max_length}")
    
    try:
        model_loader = ModelLoader(
            model_name=model_name,
            model_path=str(model_path_absolute)
        )
        model_loader.load_model()
        
        predictor = ToxicityPredictor(
            model=model_loader.get_model(),
            tokenizer=model_loader.get_tokenizer(),
            max_length=max_length,
            device=model_loader.device
        )
        
        logger.info("✅ Model loaded successfully!")
        logger.info(f"✅ Using device: {model_loader.device}")
        logger.info(f"✅ Fine-tuned model loaded: {model_loader.fine_tuned_loaded}")
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Content Moderation API",
    description="Real-time toxicity detection using DistilBERT",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Content Moderation API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    is_loaded = model_loader is not None and model_loader.is_loaded()
    fine_tuned = model_loader.fine_tuned_loaded if model_loader else False
    
    return HealthResponse(
        status="healthy",
        model_loaded=is_loaded,
        version="1.0.0"
    )


@app.post("/moderate", response_model=ModerationResponse, tags=["Moderation"])
async def moderate_content(request: ModerationRequest):
    """
    Moderate content for toxicity.
    
    Args:
        request: ModerationRequest with text to analyze
        
    Returns:
        ModerationResponse with toxicity predictions
    """
    try:
        # Validate input
        is_valid, error_msg = validate_text(request.text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Clean text
        cleaned_text = clean_text(request.text)
        
        # Check if predictor is loaded
        if predictor is None:
            raise HTTPException(
                status_code=503, 
                detail="Model not loaded. Please try again later."
            )
        
        # Get prediction
        prediction = predictor.predict(cleaned_text)
        
        # Create response
        response = ModerationResponse(
            text=request.text[:100] + "..." if len(request.text) > 100 else request.text,
            is_toxic=prediction['is_toxic'],
            toxicity_scores=ToxicityScores(**prediction['toxicity_scores']),
            flagged_categories=prediction['flagged_categories'],
            confidence=prediction['confidence'],
            timestamp=datetime.utcnow()
        )
        
        logger.info(f"Moderation request processed: is_toxic={prediction['is_toxic']}, confidence={prediction['confidence']:.3f}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)