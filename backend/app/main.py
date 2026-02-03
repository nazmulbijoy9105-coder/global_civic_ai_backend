# FastAPI main
from fastapi import FastAPI
from app.routers import questions, payments, admin

app = FastAPI(title="Moral Compass AI Backend")

app.include_router(questions.router, prefix="/api/questions")
app.include_router(payments.router, prefix="/api/payments")
app.include_router(admin.router, prefix="/api/admin")

@app.get("/")
def root():
    return {"status": "Backend Live"}
