from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_user

router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.post("/start", response_model=schemas.SessionOut, status_code=status.HTTP_201_CREATED)
def start_session(
    body: schemas.SessionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check for existing in-progress session
    existing = (
        db.query(models.AssessmentSession)
        .filter(
            models.AssessmentSession.user_id == current_user.id,
            models.AssessmentSession.status == "in_progress",
        )
        .first()
    )
    if existing:
        return existing

    new_session = models.AssessmentSession(
        user_id=current_user.id,
        total_questions=body.total_questions,
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


@router.get("/session/{session_id}", response_model=schemas.SessionOut)
def get_session(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(models.AssessmentSession)
        .filter(
            models.AssessmentSession.id == session_id,
            models.AssessmentSession.user_id == current_user.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/session/{session_id}/questions", response_model=list[schemas.QuestionOut])
def get_session_questions(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(models.AssessmentSession)
        .filter(
            models.AssessmentSession.id == session_id,
            models.AssessmentSession.user_id == current_user.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = (
        db.query(models.Question)
        .order_by(func.random())
        .limit(session.total_questions)
        .all()
    )
    return questions


@router.post("/session/{session_id}/answer", response_model=schemas.ResponseOut)
def submit_answer(
    session_id: int,
    response: schemas.ResponseCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(models.AssessmentSession)
        .filter(
            models.AssessmentSession.id == session_id,
            models.AssessmentSession.user_id == current_user.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Session already completed")

    new_response = models.Response(
        user_id=current_user.id,
        question_id=response.question_id,
        session_id=session_id,
        answer=response.answer,
        score=response.score,
    )
    db.add(new_response)

    session.current_index += 1
    if session.current_index >= session.total_questions:
        session.status = "completed"
        session.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(new_response)
    return new_response


@router.post("/session/{session_id}/complete")
def complete_session(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(models.AssessmentSession)
        .filter(
            models.AssessmentSession.id == session_id,
            models.AssessmentSession.user_id == current_user.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.status = "completed"
    session.completed_at = datetime.utcnow()
    db.commit()

    # Generate report scores
    responses = (
        db.query(models.Response)
        .filter(models.Response.session_id == session_id)
        .all()
    )
    if not responses:
        return {"message": "Session completed", "session_id": session_id, "report": {}}

    # Group by category
    category_scores: dict[str, list[float]] = {}
    for r in responses:
        question = db.query(models.Question).filter(models.Question.id == r.question_id).first()
        if question:
            cat = question.category
            category_scores.setdefault(cat, []).append(r.score)

    # Calculate average per category
    report = {}
    for cat, scores in category_scores.items():
        avg = sum(scores) / len(scores) if scores else 0
        report[cat] = {
            "average_score": round(avg, 2),
            "responses_count": len(scores),
            "max_score": max(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
        }

        # Save adaptive score
        score_entry = models.AdaptiveScore(
            session_id=session_id,
            trait=cat,
            score=round(avg, 3),
            confidence=round(1.0 - (max(scores) - min(scores)) / 4.0, 3) if len(scores) > 1 else 1.0,
        )
        db.add(score_entry)

    db.commit()

    return {"message": "Session completed", "session_id": session_id, "report": report}


@router.get("/session/{session_id}/report")
def get_report(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(models.AssessmentSession)
        .filter(
            models.AssessmentSession.id == session_id,
            models.AssessmentSession.user_id == current_user.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    scores = (
        db.query(models.AdaptiveScore)
        .filter(models.AdaptiveScore.session_id == session_id)
        .all()
    )

    responses = (
        db.query(models.Response)
        .filter(models.Response.session_id == session_id)
        .all()
    )

    total_score = sum(s.score for s in scores) / len(scores) if scores else 0
    total_responses = len(responses)

    # Generate recommendations based on scores
    recommendations = []
    score_data = {}
    for s in scores:
        score_data[s.trait] = {"score": s.score, "confidence": s.confidence}
        if s.score < 0.4:
            recommendations.append(f"Focus on improving your understanding of {s.trait}")
        elif s.score < 0.7:
            recommendations.append(f"Good progress in {s.trait} - keep learning!")
        else:
            recommendations.append(f"Excellent awareness in {s.trait}!")

    if not recommendations:
        recommendations = ["Complete more assessments to get personalized recommendations"]

    # Generate summary
    if total_score >= 0.7:
        summary = "Excellent civic and financial awareness! You demonstrate strong understanding across most areas."
    elif total_score >= 0.4:
        summary = "Good foundation in civic awareness. There are some areas where additional learning would be beneficial."
    else:
        summary = "You're starting your civic awareness journey. Focus on the recommended areas to improve your understanding."

    return {
        "session_id": session_id,
        "user_id": current_user.id,
        "status": session.status,
        "scores": score_data,
        "total_score": round(total_score, 3),
        "total_responses": total_responses,
        "summary": summary,
        "recommendations": recommendations,
        "created_at": session.created_at.isoformat(),
        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
    }


@router.get("/history")
def get_assessment_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(models.AssessmentSession)
        .filter(models.AssessmentSession.user_id == current_user.id)
        .order_by(models.AssessmentSession.created_at.desc())
        .all()
    )
    result = []
    for s in sessions:
        scores = (
            db.query(models.AdaptiveScore)
            .filter(models.AdaptiveScore.session_id == s.id)
            .all()
        )
        avg_score = sum(sc.score for sc in scores) / len(scores) if scores else 0
        result.append({
            "session_id": s.id,
            "status": s.status,
            "total_questions": s.total_questions,
            "current_index": s.current_index,
            "average_score": round(avg_score, 3),
            "created_at": s.created_at.isoformat(),
            "completed_at": s.completed_at.isoformat() if s.completed_at else None,
        })
    return result
