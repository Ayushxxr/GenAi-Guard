from fastapi import APIRouter
from pydantic import BaseModel
from app.core.model_loader import ModelLoader
from app.core.activity_logger import ActivityLogger
import os

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
from app.core.activity_logger import ActivityLogger

router = APIRouter()

class WebAnalysisRequest(BaseModel):
    url: str = None
    cookies: dict = None
    feature: str # 'phishing_site', 'cookie_integrity'

@router.post("/scan")
def scan_web(request: WebAnalysisRequest):
    risk_score = 0
    alerts = []

    # 4. Website Phishing Detection
    if request.feature == 'phishing_site' or request.feature == 'all':
        if request.url:
            # Model check
            pred = ModelLoader.predict("url_phishing_clf", request.url, model_dir=MODELS_DIR)
            if pred == 1:
                risk_score += 90
                alerts.append("Malicious Phishing URL detected by AI")
            
            # Simple Heuristic
            legit_domains = ["hdfcbank.com", "barclays.com"]
            domain_parts = request.url.split("//")[-1].split("/")[0]
            
            # Check for typosquatting (simple visual check logic for demo)
            if "hdfc" in domain_parts and domain_parts not in legit_domains:
                risk_score += 70
                alerts.append(f"Suspicious domain resembling bank: {domain_parts}")

    # 5. Cookie Manipulation Detection
    if request.feature == 'cookie_integrity' or request.feature == 'all':
        if request.cookies:
            # In a real scenario, we check the HMAC signature of the cookie
            # Here we simulate finding a modified flag or missing secure flag
            for key, val in request.cookies.items():
                if "session" in key and len(val) < 10: # malicious modification check
                    risk_score += 60
                    alerts.append(f"Suspicious localized cookie modification: {key}")

    # Log the activity
    ActivityLogger.log_activity(
        "Web Guard",
        request.feature,
        min(risk_score, 100),
        alerts
    )

    return {
        "risk_score": min(risk_score, 100),
        "alerts": alerts
    }
