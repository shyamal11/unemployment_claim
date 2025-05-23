from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Unemployment Claims API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./unemployment.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Together AI
    TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY", "")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 