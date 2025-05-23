import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unemployment.db")
        self.TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
        self.EMBEDDING_MODEL = "togethercomputer/m2-bert-80M-8k-retrieval"
        self.LLM_MODEL = "deepseek-ai/DeepSeek-R1"

settings = Settings() 