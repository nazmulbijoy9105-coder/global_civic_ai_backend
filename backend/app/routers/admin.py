from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app import models, schemas, database

router = APIRouter(prefix="/admin", tags=["Admin"])

# ✅ Get all users
@router.get("/users", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# ✅ Get all sessions
@router.get("/sessions", response_model=list[schemas.SessionOut])
def get_all_sessions(db: Session = Depends(database.get_db)):
    sessions = db.query(models.Session).all()
    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found")
    return sessions

# ✅ Get all adaptive scores
@router.get("/scores", response_model=list[schemas.AdaptiveScoreOut])
def get_all_scores(db: Session = Depends(database.get_db)):
    scores = db.query(models.AdaptiveScore).all()
    if not scores:
        raise HTTPException(status_code=404, detail="No scores found")
    return scores

# ✅ Get all audit logs
@router.get("/audits", response_model=list[schemas.AuditLogOut])
def get_all_audits(db: Session = Depends(database.get_db)):
    audits = db.query(models.AuditLog).all()
    if not audits:
        raise HTTPException(status_code=404, detail="No audit logs found")
    return audits