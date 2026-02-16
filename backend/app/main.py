from fastapi import FastAPI
from backend.app.routers import auth, payments, questions, admin, adaptive

app = FastAPI()

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "environment": "development"}

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(questions.router, prefix="/questions", tags=["questions"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(adaptive.router, prefix="/adaptive", tags=["adaptive"])