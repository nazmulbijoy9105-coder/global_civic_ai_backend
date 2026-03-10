import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Internal imports - Ensure these match your actual folder structure
from backend.app import models, schemas
from backend.app.database import get_db

load_dotenv()

# --- CONFIGURATION ---
# IMPORTANT: Set a long, random SECRET_KEY in your Render Env Group
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-dev-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Using bcrypt specifically for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- UTILS ---

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify plain password against the stored hash."""
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- ENDPOINTS ---

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user with hashed password."""
    try:
        # 1. Check if email exists
        if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already registered"
            )

        # 2. Check if username exists
        if db.query(models.User).filter(models.User.username == user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already taken"
            )

        # 3. Hash and create
        new_user = models.User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password),
            role="user"  # Default role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during registration: {str(e)}"
        )

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return a Bearer JWT."""
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use email as the subject (unique identifier)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "role": db_user.role
        }
    }