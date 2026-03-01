import csv
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/", response_model=list[schemas.QuestionOut])
def get_questions(
    category: str | None = None,
    lang: str = "en",
    db: Session = Depends(get_db),
):
    query = db.query(models.Question)
    if category:
        query = query.filter(models.Question.category == category)
    questions = query.all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions


@router.get("/random", response_model=list[schemas.QuestionOut])
def get_random_questions(
    count: int = 20,
    db: Session = Depends(get_db),
):
    from sqlalchemy.sql.expression import func

    questions = db.query(models.Question).order_by(func.random()).limit(count).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(models.Question.category).distinct().all()
    return [c[0] for c in cats]


@router.get("/{question_id}", response_model=schemas.QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.post("/seed")
def seed_questions(db: Session = Depends(get_db)):
    """Seed questions from CSV file into database."""
    existing = db.query(models.Question).count()
    if existing > 0:
        return {"message": f"Questions already seeded ({existing} found)"}

    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "questions_120.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")

    count = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = models.Question(
                category=row.get("category", "general"),
                age_group=row.get("age_group"),
                text_en=row.get("question_en", ""),
                text_bn=row.get("question_bn"),
                text_hi=row.get("question_hi"),
                text_jp=row.get("question_jp"),
                text_cn=row.get("question_cn"),
                options=row.get("options", "Always,Sometimes,Rarely,Never"),
            )
            db.add(q)
            count += 1

    db.commit()
    return {"message": f"Seeded {count} questions"}
