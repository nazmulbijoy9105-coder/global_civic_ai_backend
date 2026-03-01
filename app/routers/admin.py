from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_user, get_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/status")
def admin_status(current_user: models.User = Depends(get_current_user)):
    return {
        "is_admin": current_user.is_admin,
        "user_id": current_user.id,
        "username": current_user.username,
    }


@router.get("/users", response_model=list[schemas.UserOut])
def get_all_users(
    current_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return db.query(models.User).all()


@router.get("/sessions")
def get_all_sessions(
    current_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    sessions = db.query(models.AssessmentSession).all()
    result = []
    for s in sessions:
        user = db.query(models.User).filter(models.User.id == s.user_id).first()
        result.append({
            "id": s.id,
            "user_id": s.user_id,
            "username": user.username if user else "Unknown",
            "status": s.status,
            "total_questions": s.total_questions,
            "current_index": s.current_index,
            "created_at": s.created_at.isoformat(),
            "completed_at": s.completed_at.isoformat() if s.completed_at else None,
        })
    return result


@router.get("/scores")
def get_all_scores(
    current_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    scores = db.query(models.AdaptiveScore).all()
    return [
        {
            "id": s.id,
            "session_id": s.session_id,
            "trait": s.trait,
            "score": s.score,
            "confidence": s.confidence,
        }
        for s in scores
    ]


@router.get("/stats")
def get_stats(
    current_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    total_users = db.query(models.User).count()
    total_sessions = db.query(models.AssessmentSession).count()
    completed_sessions = (
        db.query(models.AssessmentSession)
        .filter(models.AssessmentSession.status == "completed")
        .count()
    )
    total_payments = db.query(models.PaymentHistory).count()
    total_questions = db.query(models.Question).count()

    return {
        "total_users": total_users,
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "total_payments": total_payments,
        "total_questions": total_questions,
    }


@router.post("/make-admin/{user_id}")
def make_admin(
    user_id: int,
    current_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    db.commit()
    return {"message": f"User {user.username} is now admin"}
