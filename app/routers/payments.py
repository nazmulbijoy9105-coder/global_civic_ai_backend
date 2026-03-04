from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create", response_model=schemas.PaymentHistoryOut, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: schemas.PaymentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_payment = models.PaymentHistory(
        user_id=current_user.id,
        amount=payment.amount,
        currency=payment.currency,
        payment_method=payment.payment_method,
        status="completed",
        timestamp=datetime.utcnow(),
    )
    db.add(new_payment)

    # Update user payment status
    current_user.has_paid = True
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/history", response_model=list[schemas.PaymentHistoryOut])
def get_payment_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    payments = (
        db.query(models.PaymentHistory)
        .filter(models.PaymentHistory.user_id == current_user.id)
        .order_by(models.PaymentHistory.timestamp.desc())
        .all()
    )
    return payments


@router.get("/status")
def get_payment_status(
    current_user: models.User = Depends(get_current_user),
):
    return {
        "has_paid": current_user.has_paid,
        "user_id": current_user.id,
    }
