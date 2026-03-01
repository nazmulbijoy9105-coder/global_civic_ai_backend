import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app import models
from app.database import get_db
from app.auth_utils import get_current_user

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/pdf/{session_id}")
def download_pdf_report(
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

    # Generate PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.HexColor("#0A1628"),
        spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=colors.HexColor("#00C896"),
        spaceAfter=10,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#374151"),
        spaceAfter=8,
    )

    elements = []

    # Title
    elements.append(Paragraph("Global Civic AI", title_style))
    elements.append(Paragraph("Assessment Report", heading_style))
    elements.append(Spacer(1, 12))

    # User info
    elements.append(Paragraph(f"<b>User:</b> {current_user.username}", body_style))
    elements.append(Paragraph(f"<b>Email:</b> {current_user.email}", body_style))
    elements.append(
        Paragraph(
            f"<b>Date:</b> {session.created_at.strftime('%B %d, %Y')}",
            body_style,
        )
    )
    elements.append(
        Paragraph(f"<b>Overall Score:</b> {round(total_score * 100, 1)}%", body_style)
    )
    elements.append(Spacer(1, 20))

    # Scores table
    if scores:
        elements.append(Paragraph("Score Breakdown", heading_style))
        table_data = [["Category", "Score", "Confidence"]]
        for s in scores:
            table_data.append([
                s.trait.replace("_", " ").title(),
                f"{round(s.score * 100, 1)}%",
                f"{round(s.confidence * 100, 1)}%",
            ])

        table = Table(table_data, colWidths=[3 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0A1628")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ])
        )
        elements.append(table)
        elements.append(Spacer(1, 20))

    # Summary
    if total_score >= 0.7:
        summary = "Excellent civic and financial awareness! You demonstrate strong understanding across most areas."
    elif total_score >= 0.4:
        summary = "Good foundation in civic awareness. There are some areas where additional learning would be beneficial."
    else:
        summary = "You're starting your civic awareness journey. Focus on the recommended areas to improve."

    elements.append(Paragraph("Summary", heading_style))
    elements.append(Paragraph(summary, body_style))
    elements.append(Spacer(1, 12))

    # Recommendations
    elements.append(Paragraph("Recommendations", heading_style))
    for s in scores:
        if s.score < 0.4:
            elements.append(
                Paragraph(
                    f"- Focus on improving your understanding of {s.trait.replace('_', ' ')}",
                    body_style,
                )
            )
        elif s.score < 0.7:
            elements.append(
                Paragraph(
                    f"- Good progress in {s.trait.replace('_', ' ')} - keep learning!",
                    body_style,
                )
            )
        else:
            elements.append(
                Paragraph(
                    f"- Excellent awareness in {s.trait.replace('_', ' ')}!",
                    body_style,
                )
            )

    elements.append(Spacer(1, 30))
    elements.append(
        Paragraph(
            f"<i>Generated by Global Civic AI on {datetime.utcnow().strftime('%B %d, %Y')}</i>",
            ParagraphStyle("Footer", parent=styles["Normal"], fontSize=9, textColor=colors.grey),
        )
    )

    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=civic_ai_report_{session_id}.pdf"
        },
    )
