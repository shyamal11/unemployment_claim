from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.base import Base

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    ssn_last4 = Column(String(4), index=True)
    employer = Column(String(100))
    separation_reason = Column(String)
    earnings = Column(Float)
    employment_months = Column(Integer)
    status = Column(String(20))
    fraud_score = Column(Float)
    explanation = Column(String)
    created_at = Column(DateTime, default=func.now()) 