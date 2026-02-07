import os
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter()

JWT_SECRET_CURRENT = os.getenv("JWT_SECRET_CURRENT", "your_current_secret")
JWT_SECRET_PREVIOUS = os.getenv("JWT_SECRET_PREVIOUS", "your_previous_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_users_db = {}

class UserIn(BaseModel):
    email: str
    password: str
    consent: bool

class UserOut(BaseModel):
    email: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, secret):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

def verify_token(token: str):
    for secret in [JWT_SECRET_CURRENT, JWT_SECRET_PREVIOUS]:
        try:
            payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            continue
    raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/signup", status_code=201)
def signup(user: UserIn, response: Response):
    if not user.consent:
        raise HTTPException(status_code=400, detail="Consent is required")
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.email] = {"hashed_password": hashed_password}
    access_token = create_access_token({"sub": user.email}, JWT_SECRET_CURRENT)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": form_data.username}, JWT_SECRET_CURRENT)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
    return {"message": "Logged in"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/me", response_model=UserOut)
def me(access_token: Optional[str] = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_token(access_token)
    email: str = payload.get("sub")
    if email is None or email not in fake_users_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"email": email}