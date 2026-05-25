from pydantic import BaseModel, Field
from typing import List, Optional


class CodeReviewRequest(BaseModel):
    filename: str = Field(..., example="login.py")
    language: str = Field(..., example="python")
    code: str = Field(..., example="password = 'admin123'")


class Finding(BaseModel):
    title: str
    severity: str
    line: Optional[int] = None
    category: str
    explanation: str
    recommendation: str
    matched_text: Optional[str] = None


class CodeReviewResponse(BaseModel):
    review_id: Optional[int] = None
    filename: str
    language: str
    risk_level: str
    score: int
    findings: List[Finding]
    summary: str
