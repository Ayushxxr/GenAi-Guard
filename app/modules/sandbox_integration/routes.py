from fastapi import APIRouter, HTTPException
from sandbox.executor import SandboxExecutor, TEST_PROMPTS

router = APIRouter()

from pydantic import BaseModel

class SandboxRequest(BaseModel):
    target_url: str = None

@router.post("/scan")
async def run_sandbox_audit(request: SandboxRequest = None):
    """
    Triggers the local Sandbox Executor to run security tests.
    Returns the JSON report with score and details.
    """
    try:
        executor = SandboxExecutor()
        # Ensure model is loaded
        if not executor.model:
             return {
                 "security_score": 0, 
                 "error": "Model not loaded. Please train model first.",
                 "details": []
             }

        # Run Audit with dynamic URL if provided
        target_url = request.target_url if request else None
        report = executor.run_tests(TEST_PROMPTS, target_url=target_url)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
