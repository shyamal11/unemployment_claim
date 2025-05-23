from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.services.fraud_detector import FraudDetector
from app.services.eligibility import EligibilityChecker
from app.services.llm_service import DeepSeekLLM
from app.schemas.claim import ClaimCreate, ClaimResponse
from app.db.session import get_db
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/submit", response_model=ClaimResponse)
async def submit_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received claim submission: {claim.dict()}")
        
        # Initialize services
        fraud_detector = FraudDetector()
        eligibility_checker = EligibilityChecker()
        
        # Convert claim data to dict for processing
        claim_data = claim.dict()
        logger.info(f"Processing claim data: {claim_data}")
        
        # Ensure numeric types
        claim_data['earnings'] = float(claim_data['earnings'])
        claim_data['employment_months'] = int(claim_data['employment_months'])
        logger.info(f"Converted numeric values: {claim_data}")
        
        # Perform fraud detection
        logger.info("Starting fraud detection")
        fraud_result = fraud_detector.analyze_claim(claim_data)
        logger.info(f"Fraud detection result: {fraud_result}")
        
        # Check eligibility
        logger.info("Checking eligibility")
        failed_rules = eligibility_checker.evaluate(claim_data)
        logger.info(f"Eligibility check result: {failed_rules}")
        
        # Determine status
        status = "approved" if not failed_rules else "denied"
        logger.info(f"Claim status determined: {status}")
        
        # Generate explanation
        logger.info("Generating explanation")
        llm = DeepSeekLLM()
        explanation_context = {
            "status": status,
            "fraud_analysis": fraud_result,
            "eligibility": {
                "failed_rules": [r["message"] for r in failed_rules]
            },
            "user_data": claim_data
        }
        logger.info(f"Explanation context: {explanation_context}")
        
        explanation = llm.generate_explanation(explanation_context)
        logger.info(f"Generated explanation: {explanation}")
        
        response = ClaimResponse(
            status=status,
            explanation=explanation,
            fraud_score=fraud_result["score"],
            failed_rules=[r["message"] for r in failed_rules]
        )
        logger.info(f"Final response: {response.dict()}")
        
        return response
        
    except ValueError as e:
        logger.error(f"Invalid data format: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing claim: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{ssn_last4}")
async def get_claim_history(ssn_last4: str, db: Session = Depends(get_db)):
    # Implementation for getting claim history
    pass 