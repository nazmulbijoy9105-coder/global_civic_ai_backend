from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.auth_utils import get_current_user
from app.services.adaptive_engine import AdaptivePsychometricEngine

router = APIRouter(prefix="/adaptive", tags=["Adaptive"])

# Initialize engine with question bank
question_bank = {
    "civic_awareness": [
        {"id": 1, "text": "I understand my civic rights and responsibilities.", "weight": 1.2},
        {"id": 2, "text": "I actively participate in community decisions.", "weight": 1.0},
    ],
    "financial_literacy": [
        {"id": 3, "text": "I understand basic financial planning principles.", "weight": 1.1},
        {"id": 4, "text": "I can evaluate financial risks effectively.", "weight": 1.3},
    ],
    "openness": [
        {"id": 5, "text": "I enjoy trying new experiences.", "weight": 1},
        {"id": 6, "text": "I am curious about different cultures.", "weight": 1.2},
    ],
    "empathy": [
        {"id": 7, "text": "I can easily understand others' feelings.", "weight": 1},
        {"id": 8, "text": "I often put myself in others' shoes.", "weight": 1.3},
    ],
}
engine = AdaptivePsychometricEngine(question_bank)


@router.post("/start")
def start_adaptive_session():
    engine.start_session()
    return {"message": "Adaptive session started", "traits": list(question_bank.keys())}


@router.get("/next/{trait}")
def get_next_question(trait: str):
    question = engine.next_question(trait)
    if not question:
        return {"message": "No more questions for this trait", "trait": trait}
    return question


@router.post("/answer")
def submit_answer(
    trait: str,
    question_id: int,
    score: float,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if trait not in question_bank:
        raise HTTPException(status_code=404, detail="Trait not found")

    engine.answer_question(trait, question_id, score)

    new_response = models.Response(
        user_id=current_user.id,
        question_id=question_id,
        score=score,
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)

    return {"message": "Answer recorded", "response_id": new_response.id}


@router.get("/report")
def generate_report():
    report = engine.generate_report()
    return report
