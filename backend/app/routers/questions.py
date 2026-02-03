# Questions router placeholder
from fastapi import APIRouter
import csv, random

router = APIRouter()

@router.get("/random")
def random_question():
    with open("data/questions_120.csv", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        return random.choice(reader)
