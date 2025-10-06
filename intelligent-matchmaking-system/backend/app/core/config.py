"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Intelligent Matchmaking System"
    debug: bool = False
    api_version: str = "v1"
    
    # Database settings
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "intelligent_matchmaking"
    
    # Security settings
    secret_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS settings
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"]
    
    # Email/SMTP settings
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Legacy email settings (for backward compatibility)
    email_host: Optional[str] = None
    email_port: Optional[int] = None
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    
    # ML Model settings
    ml_model_path: str = "./ml/models/"
    
    class Config:
        env_file = ".env"


settings = Settings()