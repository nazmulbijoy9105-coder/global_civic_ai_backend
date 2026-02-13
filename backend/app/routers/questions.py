from fastapi import APIRouter, HTTPException
import csv, random, os

router = APIRouter()

# Works both locally and on Render
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CSV_PATH = os.path.join(BASE_DIR, "data", "questions_120.csv")

def load_questions():
    try:
        with open(CSV_PATH, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Questions file not found at {CSV_PATH}")

@router.get("/all")
def get_all_questions():
    return load_questions()

@router.get("/random")
def random_question():
    questions = load_questions()
    return random.choice(questions)

@router.get("/assessment")
def get_assessment(limit: int = 20):
    questions = load_questions()
    return random.sample(questions, min(limit, len(questions)))
