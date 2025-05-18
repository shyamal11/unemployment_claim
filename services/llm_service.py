from together import Together
from config import settings
import json

class DeepSeekLLM:
    def __init__(self):
        self.client = Together(api_key=settings.TOGETHER_API_KEY)
    
    def generate_explanation(self, decision: str, context: dict) -> str:
        messages = [
            {
                "role": "system",
                "content": "You're an unemployment insurance assistant. Provide clear, concise explanations."
            },
            {
                "role": "user",
                "content": f"Explain this decision: {decision}\nContext: {json.dumps(context)}"
            }
        ]
        
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            max_tokens=150,
            temperature=0.3,
            stream=False  # Disable streaming for simplicity
        )
        
        return response.choices[0].message.content