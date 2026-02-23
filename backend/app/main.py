from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Import routers
from app.routers import auth, users, questions, adaptive, assessment, payments, admin

# ✅ FastAPI app metadata
app = FastAPI(
    title="Global Civic AI Backend",
    description="Transparent, Responsible AI Psychometric SaaS",
    version="1.0.0"
)

# ✅ CORS setup for production
origins = [
    "http://localhost:3000",   # local frontend
    "https://global-civic-ai-frontend.onrender.com",  # production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check endpoint
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Backend running successfully"}

# ✅ Router inclusion
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(questions.router)
app.include_router(adaptive.router)
app.include_router(assessment.router)
app.include_router(payments.router)
app.include_router(admin.router)