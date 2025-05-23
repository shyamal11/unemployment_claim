from pydantic import BaseModel
from typing import List

class ClaimCreate(BaseModel):
    ssn_last4: str
    employer: str
    separation_reason: str
    earnings: float
    employment_months: int

class ClaimResponse(BaseModel):
    status: str
    explanation: str
    fraud_score: float
    failed_rules: List[str] 