from services.embedding_service import TogetherEmbedding
from database import SessionLocal
from database.models import FraudPattern, ClaimHistory
from typing import Dict, Any, List
import json
from datetime import datetime, timedelta
import numpy as np
# Import for anomaly detector will be added once the file is created
# from services.anomaly_detector import EarningsAnomalyDetector

class FraudDetector:
    def __init__(self):
        self.embedding_model = TogetherEmbedding()
        # Initialize anomaly detector here once implemented
        # self.anomaly_detector = EarningsAnomalyDetector()

    HARD_RULES = {
        "earnings_too_high": lambda x: x['earnings'] > 20000,
        "employment_too_short": lambda x: x['employment_months'] < 1,
        "blacklisted_employers": lambda x: x['employer'] in ["Fake Corp LLC", "Shell Co"]
    }

    def apply_hard_rules(self, claim_data: Dict) -> List[str]:
        """Apply hard-coded fraud rules"""
        return [rule for rule, check in self.HARD_RULES.items() if check(claim_data)]

    def check_temporal_patterns(self, ssn_last4: str) -> bool:
        """Check for temporal patterns like frequent filing"""
        # Note: This checks for more than 3 claims in the last year for the same SSN
        with SessionLocal() as db:
            past_claims_count = db.query(ClaimHistory).filter(
                ClaimHistory.ssn_last4 == ssn_last4,
                ClaimHistory.claim_date > datetime.now() - timedelta(days=365)
            ).count()
        return past_claims_count > 3

    def _get_risk_factor(self, region: str) -> float:
        """Placeholder for regional risk factor - currently returns 1.0"""
        # This would typically involve a lookup based on applicant location/region
        return 1.0

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
        
        # Placeholder for regional risk factor - assuming a default region or applicant data includes it
        # For now, we'll just use a dummy region or omit regional factor
        # risk_factor = self._get_risk_factor(claim_data.get('region', 'default'))
        # score = min(1.0, base_score * risk_factor)
        
        score = min(1.0, base_score)

        if is_anomaly: score = min(1.0, score + 0.2)
        
        return round(score, 2)

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def analyze_claim(self, claim_data: Dict) -> Dict[str, Any]:
        """Analyze claim data using a hybrid detection approach"""
        # 1. Get embedding
        embedding = self.embedding_model.get_contextual_embedding(claim_data)
        
        with SessionLocal() as db:
            # Store claim history
            db.add(ClaimHistory(
                ssn_last4=claim_data['ssn_last4'],
                claim_date=datetime.now(),
                employer=claim_data['employer'],
                embedding=json.dumps(embedding)  # Properly serialize embedding
            ))
            db.commit()

            # 2. Find similar patterns using cosine similarity
            patterns = db.query(FraudPattern).all()
            similar_patterns = []
            for pattern in patterns:
                if isinstance(pattern.embedding, str):
                    pattern_embedding = json.loads(pattern.embedding)
                else:
                    pattern_embedding = pattern.embedding
                similarity = self.cosine_similarity(embedding, pattern_embedding)
                if similarity > 0.8:  # Threshold for similarity
                    similar_patterns.append(pattern)

            # 3. Other checks
            hard_rules = self.apply_hard_rules(claim_data)
            temporal_redflags = self.check_temporal_patterns(claim_data['ssn_last4'])
            # Anomaly detection will be called here once implemented
            # is_anomaly = self.anomaly_detector.check(claim_data)
            is_anomaly = False # Placeholder until anomaly detector is added
        
        # 4. Calculate final score
        score = self.calculate_score(similar_patterns, hard_rules, temporal_redflags, is_anomaly)

        return {
            "score": score,
            "patterns": [p.description for p in similar_patterns],
            "hard_rule_violations": hard_rules,
            "temporal_redflags": temporal_redflags,
            "is_anomaly": is_anomaly,
            "embedding": embedding # Include embedding for potential future use (e.g., feedback loop)
        } 