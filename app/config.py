import os
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/gutendex")
    
    class Config:
        env_file = ".env"

settings = Settings()