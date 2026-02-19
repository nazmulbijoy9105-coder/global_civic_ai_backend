from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from ..adaptive_engine import AdaptivePsychometricEngine

router = APIRouter(prefix="/adaptive", tags=["adaptive"])

# --- Request Schemas (local, engine-specific) ---

class StartSessionRequest(BaseModel):
    question_bank: Dict[str, List[Dict]]
    min_score: float = 1.0
    max_score: float = 5.0

class AnswerRequest(BaseModel):
    trait: str
    question_id: int
    score: float

class AuditFactorsRequest(BaseModel):
    trait: str
    factors: Dict[str, float]

# In-memory session store (one engine per session key)
sessions: Dict[str, AdaptivePsychometricEngine] = {}


@router.post("/start/{session_id}")
def start_session(session_id: str, body: StartSessionRequest):
    engine = AdaptivePsychometricEngine(
        question_bank=body.question_bank,
        min_score=body.min_score,
        max_score=body.max_score
    )
    engine.start_session()
    sessions[session_id] = engine
    return {"message": f"Session '{session_id}' started", "traits": list(body.question_bank.keys())}


@router.post("/answer/{session_id}")
def answer_question(session_id: str, body: AnswerRequest):
    engine = sessions.get(session_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Session not found")

    engine.answer_question(body.trait, body.question_id, body.score)
    next_q = engine.next_question(body.trait)

    return {
        "message": "Answer recorded",
        "next_question": next_q if next_q else None
    }


@router.post("/audit/{session_id}")
def set_audit_factors(session_id: str, body: AuditFactorsRequest):
    engine = sessions.get(session_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Session not found")

    engine.set_audit_factors(body.trait, body.factors)
    return {"message": f"Audit factors updated for trait '{body.trait}'"}


@router.get("/report/{session_id}")
def get_report(session_id: str):
    engine = sessions.get(session_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Session not found")

    report = engine.generate_report()
    return {"session_id": session_id, "report": report}


@router.delete("/session/{session_id}")
def end_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    del sessions[session_id]
    return {"message": f"Session '{session_id}' ended"}
```

**One extra step** — move the engine class into its own file so the import works cleanly. Save your `AdaptivePsychometricEngine` class as:
```
backend/app/adaptive_engine.py
```

That's it. Your full router structure is now:
```
backend/app/
├── adaptive_engine.py       ← engine class lives here
├── schemas.py
├── models.py
├── database.py
├── main.py
└── routers/
    ├── auth.py
    ├── payments.py
    ├── questions.py
    ├── admin.py
    └── adaptive.py          ← router wraps the engine