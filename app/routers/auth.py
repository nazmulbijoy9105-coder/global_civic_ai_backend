from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_admin": db_user.is_admin,
    }


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
