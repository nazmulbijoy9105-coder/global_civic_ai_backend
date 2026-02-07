import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth

app = FastAPI()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://global-civic-ai-frontend.onrender.com")
BACKEND_URL = os.getenv("BACKEND_URL", "https://global-civic-ai-backend.onrender.com")

allowed_origins = [FRONTEND_URL, BACKEND_URL] if ENVIRONMENT == "production" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")