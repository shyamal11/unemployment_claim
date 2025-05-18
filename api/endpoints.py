from fastapi import APIRouter
from services.fraud_detector import FraudDetector
from services.eligibility import EligibilityChecker
from services.llm_service import DeepSeekLLM
from database import SessionLocal
from database.models import Applicant
import json
from typing import Dict, List

router = APIRouter()

def generate_personality_explanation(status: str, context: Dict) -> str:
    """Generate explanation with personality"""
    llm = DeepSeekLLM()
    base_prompt = """
    You're Joy, a friendly unemployment insurance assistant. Explain this decision naturally:
    
    Status: {status}
    Context: {context}
    
    Tone Guidelines:
    - Approved: Warm and congratulatory
    - Denied: Empathetic but clear
    - Use simple language (8th grade level)
    - Include relevant details but avoid jargon
    - 2-3 sentences maximum
    """
    
    return llm.generate_explanation(
        base_prompt.format(status=status, context=json.dumps(context))
)

@router.post("/claims/check")
async def check_claim(claim_data: dict):
    # Initialize services
    fraud_detector = FraudDetector()
    eligibility_checker = EligibilityChecker()
    
    # Perform checks
    fraud_result = fraud_detector.analyze_claim(claim_data)
    failed_rules = eligibility_checker.evaluate(claim_data)
    
    # Determine final status
    status = "approved" if not failed_rules else "denied"
    
    # Prepare context for explanation
    explanation_context = {
        "status": status,
        "fraud_analysis": {
            "score": fraud_result["score"],
            "patterns": fraud_result["patterns"],
            "hard_rule_violations": fraud_result["hard_rule_violations"],
            "temporal_redflags": fraud_result["temporal_redflags"],
            "is_anomaly": fraud_result["is_anomaly"],
        },
        "eligibility": {
            "failed_rules": [r["message"] for r in failed_rules]
        },
        "user_data": {
            "months": claim_data.get("employment_months"),
            "earnings": claim_data.get("earnings"),
            "employer": claim_data.get("employer"),
            "reason": claim_data.get("separation_reason")
        }
    }

    # Generate personality-driven explanation
    explanation = generate_personality_explanation(status, explanation_context)
    
    # Prepare response for frontend
    return {
        "status": status,
        "fraud_score": fraud_result["score"],
        "fraud_indicators": {
             "patterns": fraud_result["patterns"],
             "hard_rule_violations": fraud_result["hard_rule_violations"],
             "temporal_redflags": fraud_result["temporal_redflags"],
             "is_anomaly": fraud_result["is_anomaly"],
        },
        "failed_rules": [r["message"] for r in failed_rules],
        "explanation": explanation
    }