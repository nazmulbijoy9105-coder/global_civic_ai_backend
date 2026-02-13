import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from backend.app.routers import auth, payment, questions, admin

# FastAPI app
app = FastAPI(
    title="Civic-Moral Psychometric Tool",
    description="Backend API for authentication, payments, and questionnaire responses",
    version="1.0.0"
)

# Environment-based CORS
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

allowed_origins = [FRONTEND_URL, BACKEND_URL] if ENVIRONMENT == "production" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT settings
class Settings(BaseModel):
    authjwt_secret_key: str = "supersecretkey"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc):
    return HTTPException(status_code=exc.status_code, detail=exc.message)

# Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(payment.router, prefix="/payment")
app.include_router(questions.router, prefix="/questions")
app.include_router(admin.router, prefix="/admin")