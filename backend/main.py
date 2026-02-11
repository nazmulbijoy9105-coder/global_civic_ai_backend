from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi_jwt_auth import AuthJWT 
from fastapi_jwt_auth.exceptions import AuthJWTException 
from pydantic import BaseModel 
import uvicorn 
 
class User(BaseModel): 
    username: str 
    password: str 
 
app = FastAPI() 
origins = ["http://localhost:3000","https://your-prod-frontend.com"] 
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]) 
 
class Settings(BaseModel): 
    authjwt_secret_key: str = "supersecretkey" 
 
@AuthJWT.load_config 
def get_config(): 
    return Settings() 
 
users = {} 
 
@app.post("/signup") 
def signup(user: User): 
    if user.username in users: 
        raise HTTPException(status_code=400, detail="User already exists") 
    users[user.username] = user.password 
    return {"msg": "Signup successful"} 
 
@app.post("/login") 
def login(user: User, Authorize: AuthJWT = None): 
    if user.username not in users or users[user.username] != user.password: 
        raise HTTPException(status_code=401, detail="Bad username or password") 
    access_token = Authorize.create_access_token(subject=user.username) 
    return {"access_token": access_token} 
 
@app.get("/me") 
def me(Authorize: AuthJWT = None): 
    Authorize.jwt_required() 
    return {"user": Authorize.get_jwt_subject()} 
 
@app.exception_handler(AuthJWTException) 
def authjwt_exception_handler(request, exc): 
    return HTTPException(status_code=exc.status_code, detail=exc.message) 
 
if __name__ == "__main__": 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
