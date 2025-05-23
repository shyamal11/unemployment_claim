from typing import Dict, Any, List
import json
from datetime import datetime, timedelta
import numpy as np
from app.db.session import SessionLocal
from app.models.fraud import FraudPattern, ClaimHistory

class FraudDetector:
    def __init__(self):
        self.HARD_RULES = {
            "earnings_too_high": lambda x: x['earnings'] > 20000,
            "employment_too_short": lambda x: x['employment_months'] < 1,
            "blacklisted_employers": lambda x: x['employer'] in ["Fake Corp LLC", "Shell Co"]
        }

    def apply_hard_rules(self, claim_data: Dict) -> List[str]:
        """Apply hard-coded fraud rules"""
        return [rule for rule, check in self.HARD_RULES.items() if check(claim_data)]

    def check_temporal_patterns(self, ssn_last4: str) -> bool:
        """Check for temporal patterns like frequent filing"""
        with SessionLocal() as db:
            past_claims_count = db.query(ClaimHistory).filter(
                ClaimHistory.ssn_last4 == ssn_last4,
                ClaimHistory.claim_date > datetime.now() - timedelta(days=365)
            ).count()
        return past_claims_count > 3

    def calculate_score(
        self,
        similar_patterns: List[FraudPattern],
        hard_rules: List[str],
        temporal_redflags: bool,
        is_anomaly: bool
    ) -> float:
        """Calculate the final fraud score based on various factors"""
        base_score = sum(p.severity * 0.1 for p in similar_patterns)
        if hard_rules: base_score += 0.5
        if temporal_redflags: base_score += 0.3
        score = min(1.0, base_score)
        if is_anomaly: score = min(1.0, score + 0.2)
        return round(score, 2)

    def analyze_claim(self, claim_data: Dict) -> Dict[str, Any]:
        """Analyze claim data using a hybrid detection approach"""
        try:
            with SessionLocal() as db:
                # Store claim history
                db.add(ClaimHistory(
                    ssn_last4=claim_data['ssn_last4'],
                    claim_date=datetime.now(),
                    employer=claim_data['employer']
                ))
                db.commit()

                # Apply hard rules
                hard_rules = self.apply_hard_rules(claim_data)
                
                # Check temporal patterns
                temporal_redflags = self.check_temporal_patterns(claim_data['ssn_last4'])
                
                # For now, we'll skip pattern matching and anomaly detection
                similar_patterns = []
                is_anomaly = False

                # Calculate final score
                score = self.calculate_score(
                    similar_patterns,
                    hard_rules,
                    temporal_redflags,
                    is_anomaly
                )

                return {
                    "score": score,
                    "patterns": [],
                    "hard_rule_violations": hard_rules,
                    "temporal_redflags": temporal_redflags,
                    "is_anomaly": is_anomaly
                }
        except Exception as e:
            raise Exception(f"Error analyzing claim: {str(e)}") 