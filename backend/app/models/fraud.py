from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.db.base import Base

class FraudPattern(Base):
    __tablename__ = "fraud_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), index=True)
    embedding = Column(JSON)
    severity = Column(Integer)

class ClaimHistory(Base):
    __tablename__ = "claim_history"
    
    id = Column(Integer, primary_key=True, index=True)
    ssn_last4 = Column(String(4), index=True)
    claim_date = Column(DateTime)
    employer = Column(String(100))
    embedding = Column(String) 