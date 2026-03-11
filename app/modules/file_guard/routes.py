from fastapi import APIRouter, File, UploadFile
from app.core.model_loader import ModelLoader
from app.core.activity_logger import ActivityLogger
import os

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
from app.core.activity_logger import ActivityLogger

router = APIRouter()

@router.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    """
    3. Attachment Verification (Pharming/Malware)
    """
    risk_score = 0
    alerts = []
    
    # Read first few bytes for magic numbers
    content = await file.read(1024) 
    
    # Check for executable signatures in disguised files
    # MZ signature for EXE
    if content.startswith(b'MZ'):
        if not file.filename.lower().endswith('.exe'):
            risk_score += 90
            alerts.append("Executable code hidden in non-exe file (High Risk)")
    
    # Model Check for Malicious Scripts inside PDF/Docs
    # This would pass the file content or features to a model
    # For demo structure:
    model_pred = ModelLoader.predict("malware_sig_model", file.filename, model_dir=MODELS_DIR) # passing filename/metadata as dummy feature
    if model_pred == 1:
        risk_score += 100
        alerts.append("Malware signature detected by AI Model")

    ActivityLogger.log_activity(
        "File Guard",
        file.filename.split('.')[-1] if '.' in file.filename else 'file',
        min(risk_score, 100),
        alerts
    )

    return {
        "filename": file.filename,
        "risk_score": min(risk_score, 100),
        "alerts": alerts,
        "is_safe": risk_score < 50
    }
