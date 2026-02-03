# Admin router placeholder
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def admin_status():
    return {"admin": "ok"}
