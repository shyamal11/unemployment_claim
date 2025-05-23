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
    
    def generate_explanation(self, prompt: str) -> str:
        """Generate explanation using Together API"""
        try:
            print(prompt)
            response = together.Complete.create(
                prompt=prompt,
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                temperature=0.5,
                max_tokens=150
            )
            if 'choices' in response and response['choices']:
                return response['choices'][0]['text'].strip()
            else:
                print(f"LLM response missing 'choices' key: {response}")
                return "I apologize, but I'm having trouble generating a response right now. Please try again later."
        except Exception as e:
            print(f"LLM error: {str(e)}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again later."