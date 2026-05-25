import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.review import Review
from app.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.services.code_scanner import CodeScanner
from app.services.risk_scoring import calculate_score, get_risk_level
from app.services.explanation import build_summary

router = APIRouter()


@router.post("", response_model=CodeReviewResponse)
def create_review(payload: CodeReviewRequest, db: Session = Depends(get_db)):
    scanner = CodeScanner()
    findings = scanner.scan(payload.code)

    score = calculate_score(findings)
    risk_level = get_risk_level(score)
    summary = build_summary(payload.filename, findings, risk_level)

    review = Review(
        filename=payload.filename,
        language=payload.language,
        risk_level=risk_level,
        score=score,
        summary=summary,
        findings_json=json.dumps(findings)
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "review_id": review.id,
        "filename": payload.filename,
        "language": payload.language,
        "risk_level": risk_level,
        "score": score,
        "findings": findings,
        "summary": summary
    }


@router.get("")
def list_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()

    return [
        {
            "id": item.id,
            "filename": item.filename,
            "language": item.language,
            "risk_level": item.risk_level,
            "score": item.score,
            "summary": item.summary,
            "created_at": item.created_at
        }
        for item in reviews
    ]


@router.get("/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return {
        "id": review.id,
        "filename": review.filename,
        "language": review.language,
        "risk_level": review.risk_level,
        "score": review.score,
        "findings": json.loads(review.findings_json),
        "summary": review.summary,
        "created_at": review.created_at
    }
