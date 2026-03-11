import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import database engine and routers
# Note: Ensure your directory structure matches 'backend/app/...' 
# or adjust these imports if you are running from within the app folder.
from backend.app.database import engine
from backend.app.routers import (
    auth,
    users,
    questions,
    adaptive,
    assessment,
    payments,
    admin,
)

# Initialize environment variables
load_dotenv()

# Setup logging for better visibility in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Global Civic AI",
    version="1.0.0",
    description="Backend API for Global Civic AI platform",
)

# --- CORS CONFIGURATION ---
# We use your production frontend URL as the default
raw_origins = os.getenv("CORS_ORIGINS", "https://global-civic-ai-frontend.onrender.com")
CORS_ORIGINS = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.get("/", tags=["Root"])
def root():
    """Welcome endpoint with useful links."""
    return {
        "message": "Welcome to Global Civic AI API",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "active"
    }

@app.get("/health", tags=["System"])
def health_check():
    """Endpoint for Render health monitoring."""
    return {
        "status": "ok",
        "service": "Global Civic AI Backend",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

# --- CORRECTED ROUTER INCLUSIONS ---
# Remove the manual 'prefix' here if your router files already have them, 
# OR keep these and remove them from the router files (auth.py, etc.)
app.include_router(auth.router, tags=["Authentication"]) # Removed prefix="/auth"
app.include_router(users.router, tags=["Users"]) # Removed prefix="/users"
app.include_router(questions.router, tags=["Questions"]) # Removed prefix="/questions"
app.include_router(adaptive.router, tags=["Adaptive Logic"])
app.include_router(assessment.router, tags=["Assessments"])
app.include_router(payments.router, tags=["Payments"])
app.include_router(admin.router, tags=["Admin"])

# --- STARTUP LOGGING ---
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Global Civic AI Backend is starting up...")
    logger.info(f"Allowing CORS Origins: {CORS_ORIGINS}")