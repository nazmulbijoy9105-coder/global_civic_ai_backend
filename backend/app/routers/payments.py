from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app import models, schemas, database

router = APIRouter(prefix="/payments", tags=["Payments"])

# ✅ Record a new payment
@router.post("/", response_model=schemas.PaymentHistoryOut, status_code=status.HTTP_201_CREATED)
def record_payment(user_id: int, amount: float, currency: str = "USD", db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    payment = models.PaymentHistory(
        user_id=user_id,
        amount=amount,
        currency=currency,
        timestamp=datetime.utcnow()
    )
    db.add(payment)

    # ✅ Update user payment status
    user.has_paid = True
    db.commit()
    db.refresh(payment)
    return payment

# ✅ Get all payments for a user
@router.get("/{user_id}", response_model=list[schemas.PaymentHistoryOut])
def get_payments(user_id: int, db: Session = Depends(database.get_db)):
    payments = db.query(models.PaymentHistory).filter(models.PaymentHistory.user_id == user_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this user")
    return payments