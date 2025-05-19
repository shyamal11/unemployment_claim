import together
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
import json

class DeepSeekLLM:
    def __init__(self):
        together.api_key = settings.TOGETHER_API_KEY
    
    def generate_explanation(self, decision: str, context: dict) -> str:
        prompt = f"""You're an unemployment insurance assistant. Provide clear, concise explanations.\n\nExplain this decision: {decision}\nContext: {json.dumps(context)}\n\n</response>"""
        response = together.Complete.create(
            prompt=prompt,
            model=settings.LLM_MODEL,
            max_tokens=150,
            temperature=0.3,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.1,
            stop=["</response>"]
        )
        return response['output']['choices'][0]['text'].strip()