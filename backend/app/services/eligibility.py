from typing import Dict, List
from app.db.session import SessionLocal
from app.models.eligibility import EligibilityRule

class EligibilityChecker:
    def __init__(self):
        self.BASE_RULES = [
            {
                "name": "minimum_earnings",
                "condition": lambda x: x['earnings'] >= 1000,
                "message": "Must have earned at least $1,000 in the last 6 months"
            },
            {
                "name": "minimum_employment",
                "condition": lambda x: x['employment_months'] >= 3,
                "message": "Must have been employed for at least 3 months"
            },
            {
                "name": "valid_separation",
                "condition": lambda x: x['separation_reason'].lower() not in ["quit", "resigned"],
                "message": "Must not have quit voluntarily"
            }
        ]

    def evaluate(self, claim_data: Dict) -> List[Dict]:
        """Evaluate claim against eligibility rules"""
        failed_rules = []
        
        # Check base rules
        for rule in self.BASE_RULES:
            if not rule["condition"](claim_data):
                failed_rules.append({
                    "name": rule["name"],
                    "message": rule["message"]
                })
        
        # Check database rules
        with SessionLocal() as db:
            db_rules = db.query(EligibilityRule).all()
            for rule in db_rules:
                # Here you would evaluate the rule condition
                # For now, we'll just check if the rule exists
                pass
        
        return failed_rules 