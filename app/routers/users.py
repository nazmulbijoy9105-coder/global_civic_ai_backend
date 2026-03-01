from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserOut)
def update_user(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.commit()
    db.refresh(current_user)
    return current_user
