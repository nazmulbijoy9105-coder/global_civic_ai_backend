from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, payments, questions, admin, adaptive, assessment

app = FastAPI(title="Global Civic AI", version="1.0.0")

# ✅ PRODUCTION CORS CONFIG (SAFE FOR RENDER)
origins = [
    "https://global-civic-ai-frontend.onrender.com",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # IMPORTANT (True causes CORS issues in many cases)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
def health():
    return {"status": "ok", "environment": "production"}

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(payments.router)
app.include_router(questions.router)
app.include_router(admin.router)
app.include_router(adaptive.router)
app.include_router(assessment.router)