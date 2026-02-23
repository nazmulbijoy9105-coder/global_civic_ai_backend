from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, database

router = APIRouter(prefix="/questions", tags=["Questions"])

# ✅ Get all questions
@router.get("/", response_model=list[schemas.QuestionOut])
def get_questions(db: Session = Depends(database.get_db)):
    questions = db.query(models.Question).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions

# ✅ Submit a response
@router.post("/responses", response_model=schemas.ResponseOut, status_code=status.HTTP_201_CREATED)
def submit_response(response: schemas.ResponseCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == response.user_id).first()
    question = db.query(models.Question).filter(models.Question.id == response.question_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    new_response = models.Response(
        user_id=response.user_id,
        question_id=response.question_id,
        score=response.score
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response