from sqlalchemy import Column, Integer, String
from app.db.base import Base

class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String(50), unique=True, index=True)
    condition = Column(String)
    message = Column(String) 