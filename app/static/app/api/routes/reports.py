import json
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.review import Review
from app.services.report_builder import build_markdown_report

router = APIRouter()


@router.get("/{review_id}/markdown")
def get_markdown_report(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    findings = json.loads(review.findings_json)

    report = build_markdown_report(
        review_id=review.id,
        filename=review.filename,
        language=review.language,
        risk_level=review.risk_level,
        score=review.score,
        findings=findings,
        summary=review.summary
    )

    return Response(
        content=report,
        media_type="text/markdown"
    )
