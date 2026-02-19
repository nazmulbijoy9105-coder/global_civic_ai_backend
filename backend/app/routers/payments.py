from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["questions"])

@router.get("/questions")
def get_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()

@router.post("/responses")
def submit_response(response: schemas.ResponseCreate, db: Session = Depends(get_db)):
    db_response = models.Response(**response.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response