import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import auth, questions, users, assessment

app = FastAPI(title="Global Civic AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://global-civic-ai-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    return {"status": "ok"}

# REGISTER ROUTERS WITHOUT EXTRA PREFIXES
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(users.router)
app.include_router(assessment.router)

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


# --- THE EXACT FIX: REMOVE DOUBLE PREFIXES ---
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(questions.router, tags=["Questions"])
app.include_router(adaptive.router, tags=["Adaptive Logic"])
app.include_router(assessment.router, tags=["Assessments"])
app.include_router(payments.router, tags=["Payments"])
app.include_router(admin.router, tags=["Admin"])

# --- STARTUP LOGGING ---
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Global Civic AI Backend is starting up...")
    logger.info(f"Allowing CORS Origins: {CORS_ORIGINS}")