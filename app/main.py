from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, users, questions, adaptive, assessment, payments, admin
from app.routers import report

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Global Civic AI",
    version="1.0.0",
    description="Backend API for Global Civic AI platform",
)

# CORS - allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Global Civic AI API", "docs": "/docs", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Include all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(questions.router)
app.include_router(adaptive.router)
app.include_router(assessment.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(report.router)
