from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, database
from app.services.adaptive_engine import AdaptivePsychometricEngine

router = APIRouter(prefix="/assessment", tags=["Assessment"])

# ✅ Starter question bank (replace with DB later)
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

# ✅ Start a new assessment session
@router.post("/start", response_model=schemas.SessionOut, status_code=status.HTTP_201_CREATED)
def start_session(user_id: int, db: Session = Depends(database.get_db)):
    engine.start_session()
    new_session = models.Session(user_id=user_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# ✅ Get next question for a trait
@router.get("/next/{trait}", response_model=schemas.QuestionOut)
def get_next_question(trait: str):
    question = engine.next_question(trait)
    if not question:
        raise HTTPException(status_code=404, detail="No next question available")
    return question

# ✅ Submit an answer
@router.post("/answer", response_model=schemas.ResponseOut, status_code=status.HTTP_201_CREATED)
def submit_answer(response: schemas.ResponseCreate, db: Session = Depends(database.get_db)):
    if response.trait not in question_bank:
        raise HTTPException(status_code=404, detail="Trait not found")

    engine.answer_question(response.trait, response.question_id, response.score)

    new_response = models.Response(
        user_id=response.user_id,
        question_id=response.question_id,
        score=response.score
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response

# ✅ Generate full report
@router.get("/report")
def generate_report(session_id: int, db: Session = Depends(database.get_db)):
    report = engine.generate_report()

    # Save adaptive scores + audit logs in DB
    for trait, data in report.items():
        score_entry = models.AdaptiveScore(
            session_id=session_id,
            trait=trait,
            score=data["score"],
            confidence=data["confidence"]
        )
        db.add(score_entry)

        for factor, value in data["audit_profile"].items():
            audit_entry = models.AuditLog(
                session_id=session_id,
                trait=trait,
                factor=factor,
                value=value
            )
            db.add(audit_entry)

    db.commit()
    return report