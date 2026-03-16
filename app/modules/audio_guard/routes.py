from fastapi import APIRouter, File, UploadFile
from app.core.model_loader import ModelLoader
from app.core.activity_logger import ActivityLogger
import os

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
from app.core.activity_logger import ActivityLogger

router = APIRouter()

@router.post("/detect-voice")
async def detect_deepfake(file: UploadFile = File(...)):
    """
    6. Deepfake Voice Scam Detection
    Expects audio file.
    """
    # In production: Load audio, extract MFCC features, pass to model
    # Here: Structure only
    
    alerts = []
    risk = 0
    
    # Mocking Feature Extraction
    # features = extract_mfcc(file)
    # result = ModelLoader.predict("voice_auth_model", features)
    
    # Dummy logic for structure
    # Dummy logic for structure
    result = ModelLoader.predict("voice_auth_model", "dummy_audio_features", model_dir=MODELS_DIR)
    
    if result == 1: # Fake
        risk = 95
        alerts.append("AI-Generated Voice (Deepfake) Detected")
    else:
        # Fallback if model not loaded
        # alerts.append("Model not loaded - Cannot verify voice integrity") # Optional
        pass
        
    ActivityLogger.log_activity(
        "Audio Guard",
        "audio",
        min(risk, 100),
        alerts
    )
        
    return {
        "filename": file.filename,
        "is_deepfake": risk > 50,
        "risk_score": min(risk, 100),
        "alerts": alerts
    }
