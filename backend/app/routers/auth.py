from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my-webhook-secret")


def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Register
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        has_paid=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Login
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not db_user.has_paid:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Payment required")

    access_token = create_access_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": db_user.id, "email": db_user.email}
    }


# Mark user as paid
@router.post("/mark-paid/{user_id}")
def mark_paid(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.has_paid = True
    db.commit()
    db.refresh(user)
    return {"message": "Payment status updated", "user": {"id": user.id, "email": user.email, "has_paid": user.has_paid}}


# Webhook
@router.post("/payment-webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db), secret: str = None):
    if secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized webhook")

    payload = await request.json()
    user_id = payload.get("user_id")
    provider = payload.get("provider", "unknown")
    amount = payload.get("amount", 0.0)
    payment_status = payload.get("status")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    payment = models.PaymentHistory(
        user_id=user.id,
        provider=provider,
        amount=amount,
        status=payment_status,
    )
    db.add(payment)

    if payment_status == "success":
        user.has_paid = True

    db.commit()
    db.refresh(user)
    return {"message": f"Payment recorded ({payment_status})", "user": {"id": user.id, "email": user.email, "has_paid": user.has_paid}}


# Payment history
@router.get("/payments/{user_id}")
def get_payments(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(models.PaymentHistory).filter(models.PaymentHistory.user_id == user_id).all()
    if not payments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No payments found")
    return payments