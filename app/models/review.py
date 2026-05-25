from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    language = Column(String(50), nullable=False)
    risk_level = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)
    summary = Column(Text, nullable=False)
    findings_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
