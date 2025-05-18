from database import SessionLocal
from database.models import FraudPattern, Applicant
from services.anomaly_detector import EarningsAnomalyDetector # Assuming it's initialized/loaded elsewhere
from typing import List, Dict
from datetime import datetime, timedelta
import random # Assuming random might be needed for placeholder embedding

# Placeholder function to get all claims - ideally optimized for large datasets
def get_all_claims() -> List[Dict]:
    with SessionLocal() as db:
        # Fetching all claims might be inefficient in a real system
        all_applicants = db.query(Applicant).all()
        # Convert to a list of dictionaries, including placeholder embedding if not stored
        claims_data = []
        for app in all_applicants:
            claims_data.append({
                "ssn_last4": app.ssn_last4,
                "employer": app.employer,
                "separation_reason": app.separation_reason,
                "earnings": app.earnings,
                "employment_months": app.employment_months,
                "status": app.status,
                "fraud_score": app.fraud_score,
                # Use stored embedding or generate a placeholder if not available
                "embedding": app.separation_embedding if app.separation_embedding else [random.uniform(0, 1) for _ in range(384)]
            })
        return claims_data

def update_fraud_patterns(approved_claims: List[Dict], denied_claims: List[Dict]):
    """Update fraud patterns and potentially retrain models based on claim outcomes"""
    with SessionLocal() as db:
        # Add new patterns from confirmed fraud cases
        for claim in denied_claims:
            # Example condition: High fraud score for a denied claim
            if claim['fraud_score'] > 0.8:
                print(f"Adding new potential fraud pattern from denied claim (SSN: {claim['ssn_last4']})")
                # Ensure embedding exists, use placeholder if not
                embedding_data = claim.get('embedding', [random.uniform(0, 1) for _ in range(384)])
                
                new_pattern = FraudPattern(
                    description=f"System identified: {claim.get('employer','Unknown')} - {claim.get('separation_reason','')[:50]}...",
                    embedding=embedding_data,
                    severity=max(1, int(claim['fraud_score'] * 5)) # Severity based on score
                )
                db.add(new_pattern)
                
        db.commit()
    
    # Placeholder for retraining anomaly detector
    # This part would need a trained anomaly detector instance and potentially
    # more sophisticated data handling (e.g., only using approved claims for retraining inlier model)
    # try:
    #     print("Retraining anomaly detector (placeholder)...")
    #     all_claims_data = get_all_claims()
    #     anomaly_detector_instance = EarningsAnomalyDetector() # Or load a persistent instance
    #     # Prepare data in the format expected by IsolationForest.fit
    #     # features_for_training = np.array([[c.get('earnings', 0.0), c.get('employment_months', 0), len(c.get('employer', ''))] for c in all_claims_data])
    #     # anomaly_detector_instance.retrain(features_for_training)
    #     print("Anomaly detector retraining placeholder complete.")
    # except Exception as e:
    #     print(f"Anomaly detector retraining failed: {e}")

# Note: This update_fraud_patterns function would need to be called periodically
# or after processing a batch of claims within the main application flow. 