from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="GenAI Guard - Security System for Barclays Hackathon",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Dashboard
app.mount("/dashboard", StaticFiles(directory="app/simple_dashboard", html=True), name="dashboard")

# Include Routers
from app.modules.text_guard import routes as text_routes
from app.modules.web_guard import routes as web_routes
from app.modules.file_guard import routes as file_routes
from app.modules.audio_guard import routes as audio_routes
from app.core import feedback_loop

app.include_router(text_routes.router, prefix="/api/v1/text", tags=["Text Guard"])
app.include_router(web_routes.router, prefix="/api/v1/web", tags=["Web Guard"])
app.include_router(file_routes.router, prefix="/api/v1/file", tags=["File Guard"])
app.include_router(audio_routes.router, prefix="/api/v1/audio", tags=["Audio Guard"])
app.include_router(audio_routes.router, prefix="/api/v1/audio", tags=["Audio Guard"])
from app.modules.sandbox_integration import routes as sandbox_routes
app.include_router(sandbox_routes.router, prefix="/api/v1/sandbox", tags=["Sandbox"])
app.include_router(feedback_loop.router, prefix="/api/v1/feedback", tags=["Feedback Loop"])

from app.core.activity_logger import ActivityLogger

@app.get("/api/v1/history")
def get_history():
    return ActivityLogger.get_logs()

@app.get("/")
def read_root():
    return {
        "message": "GenAI Guard is running", 
        "dashboard_url": "http://localhost:8000/dashboard",
        "modules_active": ["Text", "Web", "File", "Audio"],
        "sandbox_status": "Run 'python sandbox/app.py' to start sandbox"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
