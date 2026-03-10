from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app import models, schemas, database
from backend.app.database import get_db
from backend.app.services.adaptive_engine import AdaptivePsychometricEngine

router = APIRouter(prefix="/adaptive", tags=["Adaptive"])

# ✅ Initialize engine with empty question bank (replace with DB later)
question_bank = {
    "openness": [
        {"id": 1, "text": "I enjoy trying new experiences.", "weight": 1},
        {"id": 2, "text": "I am curious about different cultures.", "weight": 1.2},
    ],
    "empathy": [
        {"id": 3, "text": "I can easily understand others' feelings.", "weight": 1},
        {"id": 4, "text": "I often put myself in others' shoes.", "weight": 1.3},
    ],
}
engine = AdaptivePsychometricEngine(question_bank)
engine.start_session()

# ✅ Get next question for a trait
@router.get("/next_question/{trait}")
def get_next_question(trait: str):
    question = engine.next_question(trait)
    if not question:
        raise HTTPException(status_code=404, detail="No next question available")
    return question

# ✅ Submit an answer
@router.post("/answer")
def submit_answer(trait: str, question_id: int, score: float, db: Session = Depends(get_db)):
    if trait not in question_bank:
        raise HTTPException(status_code=404, detail="Trait not found")

    engine.answer_question(trait, question_id, score)

    # Save response in DB
    new_response = models.Response(
        user_id=1,  # 🔑 Replace with current user from JWT later
        question_id=question_id,
        score=score
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)

    return {"message": "Answer recorded", "response_id": new_response.id}

# ✅ Set audit factors
@router.post("/set_audit/{trait}")
def set_audit(trait: str, factors: dict):
    if trait not in question_bank:
        raise HTTPException(status_code=404, detail="Trait not found")

    engine.set_audit_factors(trait, factors)
    return {"message": "Audit factors updated", "trait": trait, "factors": factors}

# ✅ Generate full report
@router.get("/report")
def generate_report(db: Session = Depends(get_db)):
    report = engine.generate_report()

    # Save adaptive scores + audit logs in DB
    for trait, data in report.items():
        score_entry = models.AdaptiveScore(
            session_id=1,  # 🔑 Replace with current session later
            trait=trait,
            score=data["score"],
            confidence=data["confidence"]
        )
        db.add(score_entry)

        for factor, value in data["audit_profile"].items():
            audit_entry = models.AuditLog(
                session_id=1,  # 🔑 Replace with current session later
                trait=trait,
                factor=factor,
                value=value
            )
            db.add(audit_entry)

    db.commit()
    return report