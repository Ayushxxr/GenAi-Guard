from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.model_loader import ModelLoader
from app.core.pii_scrubber import PIIScrubber
import re
import os

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

from app.core.activity_logger import ActivityLogger

router = APIRouter()

class TextAnalysisRequest(BaseModel):
    text: str
    check_type: str  # 'phishing', 'credentials', 'injection'

@router.post("/analyze")
def analyze_text(request: TextAnalysisRequest):
    """
    Analyzes text for:
    1. Phishing patterns (Modle: phishing_clf)
    2. Credential Leaks (Regex/NER)
    3. Prompt Injection (Model: injection_clf)
    """
    request.text
    try:
        # PRIVACY FIRST: Anonymize data before any logging/storage
        # Note: In a real flow, we might need the raw text for detection, 
        # but we ensure we NEVER log the raw text.
        scrubbed_text = PIIScrubber.scrub(request.text)
        print(f"Processing secure request: {scrubbed_text[:50]}...") # Log only scrubbed
    except Exception:
        pass

    text = request.text
    risk_score = 0
    alerts = []

    # 1. Phishing Detection
    if request.check_type == 'phishing' or request.check_type == 'all':
        # Try loading model
        model_prediction = ModelLoader.predict("phishing_clf", text, model_dir=MODELS_DIR)
        if model_prediction:
            if model_prediction == 1: # Assuming 1 is phishing
                risk_score += 80
                alerts.append("AI-Generated Phishing detected")
        else:
            # Fallback Heuristics
            urgent_keywords = ["urgent", "verify now", "account blocked", "click here"]
            if any(k in text.lower() for k in urgent_keywords):
                risk_score += 40
                alerts.append("Suspicious urgent language detected")

    # 2. Credential Leak Detection
    if request.check_type == 'credentials' or request.check_type == 'all':
        # Regex for patterns
        patterns = {
            "API Key": r"sk-[a-zA-Z0-9]{32,}",
            "Email": r"[^@]+@[^@]+\.[^@]+",
            "Password": r"password\s*=\s*['\"][^\"]+['\"]"
        }
        for p_name, p_regex in patterns.items():
            if re.search(p_regex, text, re.IGNORECASE):
                risk_score += 90
                alerts.append(f"Potential {p_name} exposed")

    # 3. Prompt Injection
    if request.check_type == 'injection' or request.check_type == 'all':
        model_prediction = ModelLoader.predict("injection_clf", text, model_dir=MODELS_DIR)
        if model_prediction == 1:
            risk_score += 100
            alerts.append("Prompt Injection Attack detected")
        else:
            # Heuristic
            if "ignore previous instructions" in text.lower():
                risk_score += 80
                alerts.append("Potential Prompt Injection keyword detected")

    # Calculate final status
    final_status = "SAFE" if risk_score < 50 else "THREAT"
    
    # Log the activity
    ActivityLogger.log_activity(
        "Text Guard",
        request.check_type,
        min(risk_score, 100),
        alerts
    )

    return {
        "risk_score": min(risk_score, 100),
        "alerts": alerts,
        "status": final_status
    }
