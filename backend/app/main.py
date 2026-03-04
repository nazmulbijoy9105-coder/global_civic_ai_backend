from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.app.routers import (
    auth,
    users,
    questions,
    adaptive,
    assessment,
    payments,
    admin,
)

load_dotenv()

app = FastAPI(
    title="Global Civic AI",
    version="1.0.0",
    description="Backend API for Global Civic AI platform",
)

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Global Civic AI API", "docs": "/docs", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Global Civic AI Backend"}


# Include all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(questions.router)
app.include_router(adaptive.router)
app.include_router(assessment.router)
app.include_router(payments.router)
app.include_router(admin.router)
