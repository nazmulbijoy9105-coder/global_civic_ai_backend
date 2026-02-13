import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import auth, payment, questions, admin

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Hide docs in production
docs_url = None if ENVIRONMENT == "production" else "/docs"
redoc_url = None if ENVIRONMENT == "production" else "/redoc"

# FastAPI app
app = FastAPI(
    title="Civic-Moral Psychometric Tool",
    description="Backend API for authentication, payments, and questionnaire responses",
    version="1.0.0",
    docs_url=docs_url,
    redoc_url=redoc_url
)

# CORS
allowed_origins = [FRONTEND_URL] if ENVIRONMENT == "production" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(payment.router, prefix="/payment")
app.include_router(questions.router, prefix="/questions")
app.include_router(admin.router, prefix="/admin")

# Health check
@app.get("/health")
def health():
    return {"status": "ok", "environment": ENVIRONMENT}
