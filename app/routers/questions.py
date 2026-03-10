import csv
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

# Ensure these match your actual folder structure
from backend.app import models, schemas
from backend.app.database import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/", response_model=list[schemas.QuestionOut])
def get_questions(
    category: str | None = None,
    db: Session = Depends(get_db),
):
    """Retrieve all questions, optionally filtered by category."""
    query = db.query(models.Question)
    if category:
        query = query.filter(models.Question.category == category)
    
    questions = query.all()
    return questions

@router.get("/random", response_model=list[schemas.QuestionOut])
def get_random_questions(
    count: int = 20,
    db: Session = Depends(get_db),
):
    """Get a random set of questions for the assessment."""
    questions = db.query(models.Question).order_by(func.random()).limit(count).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found in database")
    return questions

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """List all unique question categories."""
    cats = db.query(models.Question.category).distinct().all()
    return [c[0] for c in cats]

@router.get("/{question_id}", response_model=schemas.QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get a single question by ID."""
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

@router.post("/seed", status_code=status.HTTP_201_CREATED)
def seed_questions(db: Session = Depends(get_db)):
    """Seed questions from CSV file into the Render database."""
    # 1. Prevent duplicate seeding
    existing = db.query(models.Question).count()
    if existing > 0:
        return {"message": f"Database already has {existing} questions. Seed aborted."}

    # 2. Locate CSV - Logic to find 'data/questions_120.csv' relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "questions_120.csv")

    if not os.path.exists(csv_path):
        raise HTTPException(
            status_code=404, 
            detail=f"CSV file not found at {csv_path}. Please ensure it is in the 'backend/data' folder."
        )

    count = 0
    try:
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
            return {"message": f"Successfully seeded {count} questions from CSV."}
            
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error seeding database: {str(e)}"
        )