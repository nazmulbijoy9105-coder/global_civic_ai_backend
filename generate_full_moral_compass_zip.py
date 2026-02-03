import os
import zipfile

package_name = 'moral_compass_ai_deployable.zip'

# Folders
folders = [
    'backend/app/routers',
    'data',
    'frontend',
    'admin',
    'docs'
]

# Create folder structure
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    with open(f'{folder}/README.txt', 'w', encoding='utf-8') as f:
        f.write(f"This folder is {folder} for Moral Compass AI deployment.\n")

# Backend placeholder files
backend_files = {
    'backend/app/main.py': '# FastAPI main\nfrom fastapi import FastAPI\nfrom app.routers import questions, payments, admin\n\napp = FastAPI(title="Moral Compass AI Backend")\n\napp.include_router(questions.router, prefix="/api/questions")\napp.include_router(payments.router, prefix="/api/payments")\napp.include_router(admin.router, prefix="/api/admin")\n\n@app.get("/")\ndef root():\n    return {"status": "Backend Live"}\n',
    'backend/app/models.py': '# Pydantic models placeholder\nfrom pydantic import BaseModel\n\nclass Question(BaseModel):\n    id: int\n    category: str\n    age_group: str\n    question_en: str\n    question_bn: str\n    question_hi: str\n    question_jp: str\n    question_cn: str\n    options: str\n\nclass Payment(BaseModel):\n    user_id: str\n    amount: float\n    currency: str\n',
    'backend/app/routers/questions.py': '# Questions router placeholder\nfrom fastapi import APIRouter\nimport csv, random\n\nrouter = APIRouter()\n\n@router.get("/random")\ndef random_question():\n    with open("data/questions_120.csv", encoding="utf-8") as f:\n        reader = list(csv.DictReader(f))\n        return random.choice(reader)\n',
    'backend/app/routers/payments.py': '# Payments router placeholder\nfrom fastapi import APIRouter\nfrom app.models import Payment\n\nrouter = APIRouter()\n\n@router.post("/create")\ndef create_payment(payment: Payment):\n    return {"status": "success", "amount": payment.amount, "currency": payment.currency}\n',
    'backend/app/routers/admin.py': '# Admin router placeholder\nfrom fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get("/status")\ndef admin_status():\n    return {"admin": "ok"}\n',
    'backend/requirements.txt': 'fastapi\nuvicorn\npython-dotenv\n',
    'backend/runtime.txt': 'python-3.10.12\n',
    'backend/.env.example': 'PAYMENT_KEY=your_key_here\nADMIN_SECRET=change_me\n'
}

for path, content in backend_files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Data CSV
csv_path = 'data/questions_120.csv'
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write('id,category,age_group,question_en,question_bn,question_hi,question_jp,question_cn,options\n')
    for i in range(1, 121):
        f.write(f'{i},Category{i},AgeGroup{i},QuestionEN{i},QuestionBN{i},QuestionHI{i},QuestionJP{i},QuestionCN{i},"Always,Sometimes,Rarely,Never"\n')

# Frontend placeholders
frontend_files = [
    'frontend/pages.txt',
    'frontend/api_connections.txt',
    'frontend/payment_flow.txt',
    'frontend/multilingual_logic.txt'
]
for file in frontend_files:
    with open(file, 'w', encoding='utf-8') as f:
        f.write(f"This is placeholder for {file}\n")

# Admin placeholders
admin_files = [
    'admin/dashboard_templates.txt',
    'admin/revenue_tracking.txt'
]
for file in admin_files:
    with open(file, 'w', encoding='utf-8') as f:
        f.write(f"This is placeholder for {file}\n")

# Docs placeholders
docs_files = [
    'docs/deployment_aws_gcp.txt',
    'docs/launch_guide.txt',
    'docs/compliance_notes.txt'
]
for file in docs_files:
    with open(file, 'w', encoding='utf-8') as f:
        f.write(f"This is placeholder for {file}\n")

# Create zip
with zipfile.ZipFile(package_name, 'w') as zipf:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') or file.endswith('.txt') or file.endswith('.csv'):
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), '.'))

print(f'✅ Full deployable package generated: {package_name}')
