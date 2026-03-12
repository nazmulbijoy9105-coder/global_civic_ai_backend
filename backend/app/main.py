import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. Import all routers correctly
from backend.app.routers import (
    auth, 
    questions, 
    users, 
    assessment, 
    adaptive, 
    payments, 
    admin
)

# 2. Initialize environment variables
load_dotenv()

# 3. Setup logging for Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 4. Initialize ONE FastAPI instance
app = FastAPI(
    title="Global Civic AI",
    version="1.0.0",
    description="Backend API for Global Civic AI platform",
)

# 5. --- CORS CONFIGURATION ---
# Default to production URL if env var is missing
raw_origins = os.getenv("CORS_ORIGINS", "https://global-civic-ai-frontend.onrender.com")
CORS_ORIGINS = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. --- BASE ROUTES ---
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Global Civic AI API",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "active"
    }

@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}

# 7. --- REGISTER ROUTERS ---
# Note: Ensure your router files (e.g., auth.py) define their internal prefixes
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(questions.router, tags=["Questions"])
app.include_router(adaptive.router, tags=["Adaptive Logic"])
app.include_router(assessment.router, tags=["Assessments"])
app.include_router(payments.router, tags=["Payments"])
app.include_router(admin.router, tags=["Admin"])

# 8. --- STARTUP LOGGING ---
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Global Civic AI Backend is starting up...")
    logger.info(f"Allowing CORS Origins: {CORS_ORIGINS}")