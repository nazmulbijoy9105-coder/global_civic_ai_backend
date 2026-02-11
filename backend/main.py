from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Config CORS dynamically
origins = [
    "http://localhost:3000",
    "https://your-prod-frontend.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Settings(BaseModel):
    authjwt_secret_key: str = "CHANGE_THIS_SECRET"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.post("/signup")
def signup(user: dict):
    return {"msg": "signup success", "user": user}

@app.post("/login")
def login(user: dict, Authorize: AuthJWT = None):
    return {"msg": "login success", "user": user}

@app.get("/me")
def me():
    return {"user": "current_user"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
