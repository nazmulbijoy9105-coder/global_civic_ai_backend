from fastapi import FastAPI
from backend.app.routers import (
    auth,
    users,
    questions,
    adaptive,
    assessment,
    payments,
    admin
)

app = FastAPI(
    title="Global Civic AI",
    version="1.0.0",
    description="Backend API for Global Civic AI platform"
)

# ✅ Include all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(questions.router)
app.include_router(adaptive.router)
app.include_router(assessment.router)
app.include_router(payments.router)
app.include_router(admin.router)

# ✅ Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}