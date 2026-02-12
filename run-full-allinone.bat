@echo off
SETLOCAL

REM ----- FRONTEND -----
echo ==== FRONTEND SETUP ====
cd frontend
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

REM Fix lib/api.js
echo const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ^|^| 'http://localhost:8000'; > lib/api.js
echo. >> lib/api.js
echo class APIClient { >> lib/api.js
echo     async request(endpoint, options = {}) { >> lib/api.js
echo         const url = ^"%API_BASE_URL%^^%endpoint%^^"; >> lib/api.js
echo         const config = {...options, headers:{'Content-Type':'application/json', ...options.headers}, credentials:'include'}; >> lib/api.js
echo         try { >> lib/api.js
echo             const response = await fetch(url, config); >> lib/api.js
echo             const data = await response.json(); >> lib/api.js
echo             if (!response.ok) throw new Error(data.detail ^|^| 'API request failed'); >> lib/api.js
echo             return data; >> lib/api.js
echo         } catch(e){ console.error('API Error:', e); throw e;} >> lib/api.js
echo     } >> lib/api.js
echo     async signup(userData){ return this.request('/signup', {method:'POST', body:JSON.stringify(userData)});} >> lib/api.js
echo     async login(credentials){ return this.request('/login', {method:'POST', body:JSON.stringify(credentials)});} >> lib/api.js
echo     async logout(){ return this.request('/logout', {method:'POST'});} >> lib/api.js
echo     async getCurrentUser(){ return this.request('/me');} >> lib/api.js
echo } >> lib/api.js
echo export const api = new APIClient(); >> lib/api.js

git add lib/api.js .env.local
git commit -m "Frontend: fix API client + set dev backend"
git push origin main

start "" "http://localhost:3000/signup"
start cmd /k "npm run dev"

REM ----- BACKEND -----
cd ../backend
echo ==== BACKEND SETUP ====
echo CORS_ORIGINS=http://localhost:3000,https://your-prod-frontend.com > .env
powershell -Command "$s=openssl rand -hex 32; Add-Content -Path '.env' -Value ('SECRET_KEY=' + $s)"

REM Fix main.py
echo from fastapi import FastAPI, HTTPException > main.py
echo from fastapi.middleware.cors import CORSMiddleware >> main.py
echo from fastapi_jwt_auth import AuthJWT >> main.py
echo from fastapi_jwt_auth.exceptions import AuthJWTException >> main.py
echo from pydantic import BaseModel >> main.py
echo import uvicorn >> main.py
echo. >> main.py
echo class User(BaseModel): >> main.py
echo     username: str >> main.py
echo     password: str >> main.py
echo. >> main.py
echo app = FastAPI() >> main.py
echo origins = ["http://localhost:3000","https://your-prod-frontend.com"] >> main.py
echo app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]) >> main.py
echo. >> main.py
echo class Settings(BaseModel): >> main.py
echo     authjwt_secret_key: str = "supersecretkey" >> main.py
echo. >> main.py
echo @AuthJWT.load_config >> main.py
echo def get_config(): >> main.py
echo     return Settings() >> main.py
echo. >> main.py
echo users = {} >> main.py
echo. >> main.py
echo @app.post("/signup") >> main.py
echo def signup(user: User): >> main.py
echo     if user.username in users: >> main.py
echo         raise HTTPException(status_code=400, detail="User already exists") >> main.py
echo     users[user.username] = user.password >> main.py
echo     return {"msg": "Signup successful"} >> main.py
echo. >> main.py
echo @app.post("/login") >> main.py
echo def login(user: User, Authorize: AuthJWT = None): >> main.py
echo     if user.username not in users or users[user.username] != user.password: >> main.py
echo         raise HTTPException(status_code=401, detail="Bad username or password") >> main.py
echo     access_token = Authorize.create_access_token(subject=user.username) >> main.py
echo     return {"access_token": access_token} >> main.py
echo. >> main.py
echo @app.get("/me") >> main.py
echo def me(Authorize: AuthJWT = None): >> main.py
echo     Authorize.jwt_required() >> main.py
echo     return {"user": Authorize.get_jwt_subject()} >> main.py
echo. >> main.py
echo @app.exception_handler(AuthJWTException) >> main.py
echo def authjwt_exception_handler(request, exc): >> main.py
echo     return HTTPException(status_code=exc.status_code, detail=exc.message) >> main.py
echo. >> main.py
echo if __name__ == "__main__": >> main.py
echo     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) >> main.py

git add .env main.py
git commit -m "Backend: setup CORS, JWT, signup/login, docs"
git push origin main

start "" "http://127.0.0.1:8000/docs"
start cmd /k "python main.py"

ENDLOCAL