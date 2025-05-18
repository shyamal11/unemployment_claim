from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY")
    EMBEDDING_MODEL: str = "togethercomputer/m2-bert-80M-8k-retrieval"
    LLM_MODEL: str = "deepseek-ai/DeepSeek-R1"
    
    class Config:
        env_file = ".env"

settings = Settings() 