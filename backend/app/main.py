from fastapi import FastAPI
from backend.app.routers import auth, payments, questions, admin, adaptive

app = FastAPI(title="Global Civic AI", version="1.0.0")

# Health check
@app.get("/health")
def health():
    return {"status": "ok", "environment": "development"}

# Include routers (no prefix/tags here — already set in each router)
app.include_router(auth.router)
app.include_router(payments.router)
app.include_router(questions.router)
app.include_router(admin.router)
app.include_router(adaptive.router)