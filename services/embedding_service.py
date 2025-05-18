import requests
from config import settings
from typing import List, Dict
import json

class TogetherEmbedding:
    def get_embedding(self, text: str) -> List[float]:
        try:
            response = requests.post(
                "https://api.together.xyz/api/v1/embeddings",
                headers={"Authorization": f"Bearer {settings.TOGETHER_API_KEY}"},
                json={
                    "model": settings.EMBEDDING_MODEL,
                    "input": text
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            print(f"Embedding error: {str(e)}")
            return [0.0] * 384  # Return zero vector on failure

    def get_contextual_embedding(self, claim_data: Dict) -> List[float]:
        """Generate embedding from MULTIPLE claim aspects"""
        # Note: _get_industry_avg is not implemented, using raw earnings value
        context = f"""
Employer: {claim_data['employer']}
Reason: {claim_data['separation_reason']}
Earnings: {claim_data['earnings']}
Employment Duration: {claim_data['employment_months']} months
"""
        return self.get_embedding(context) 