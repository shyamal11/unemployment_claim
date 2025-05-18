from database import SessionLocal
from database.models import EligibilityRule
from typing import List, Dict

class EligibilityChecker:
    def evaluate(self, applicant_data: Dict) -> List[Dict]:
        failed_rules = []
        
        with SessionLocal() as db:
            rules = db.query(EligibilityRule).all()
            for rule in rules:
                try:
                    if not eval(rule.condition, {}, applicant_data):
                        failed_rules.append({
                            "rule": rule.rule_name,
                            "message": rule.message
                        })
                except:
                    continue
                    
        return failed_rules 