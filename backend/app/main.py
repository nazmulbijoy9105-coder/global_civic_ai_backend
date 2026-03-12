import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from backend.app.routers import auth, questions, users, assessment, adaptive, payments, admin

app = FastAPI(title="Global Civic AI", version="1.0.0")

raw_origins = os.getenv("CORS_ORIGINS", "https://global-civic-ai-frontend.onrender.com")
CORS_ORIGINS = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Global Civic AI API", "status": "active"}

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(questions.router, tags=["Questions"])
app.include_router(adaptive.router, tags=["Adaptive Logic"])
app.include_router(assessment.router, tags=["Assessments"])
app.include_router(payments.router, tags=["Payments"])
app.include_router(admin.router, tags=["Admin"])

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Backend starting up...")
