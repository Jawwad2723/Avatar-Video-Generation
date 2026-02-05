"""
Configuration Module
Manages environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # D-ID Configuration (Avatar Video Generation)
    DID_API_KEY: str = os.getenv("DID_API_KEY", "")
    DID_BASE_URL: str = "https://api.d-id.com"
    
    # D-ID Avatar Settings
    DID_PRESENTER_ID: str = os.getenv("DID_PRESENTER_ID", "amy-jcwCkr1grs")
    DID_VOICE_ID: str = os.getenv("DID_VOICE_ID", "en-US-JennyNeural")
    
    # News Scraping Configuration - Extended list for better reliability
    NEWS_SOURCES: list = [
        # Major International News
        "https://www.bbc.com/news",
        "https://apnews.com",
        "https://www.aljazeera.com",
        "https://www.dw.com/en",
        "https://www.france24.com/en",
        
        # US News
        "https://www.npr.org/sections/news",
        "https://abcnews.go.com",
        "https://www.cbsnews.com",
        "https://www.nbcnews.com",
        "https://www.usatoday.com",
        "https://thehill.com",
        
        # UK News
        "https://www.theguardian.com/international",
        "https://www.independent.co.uk",
        "https://www.telegraph.co.uk",
        "https://www.standard.co.uk",
        
        # Business & Tech News
        "https://www.cnbc.com",
        "https://www.bloomberg.com",
        "https://techcrunch.com",
        "https://www.wired.com",
        "https://arstechnica.com",
        
        # Science & Health
        "https://www.scientificamerican.com",
        "https://www.newscientist.com",
        "https://medicalxpress.com",
        
        # Alternative sources (if above fail)
        "https://www.axios.com",
        "https://www.politico.com",
        "https://time.com",
        "https://www.newsweek.com",
        "https://www.economist.com",
        "https://www.forbes.com"
    ]
    
    # User Agent for web scraping
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Request timeout in seconds
    REQUEST_TIMEOUT: int = 30
    
    # Application Settings
    APP_NAME: str = "AI News Avatar Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Validation function
def validate_settings():
    """
    Validate that all required settings are configured
    """
    errors = []
    
    if not settings.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set")
    
    if not settings.DID_API_KEY:
        errors.append("DID_API_KEY is not set")
    
    if errors:
        error_message = "Configuration errors:\n" + "\n".join(f"- {error}" for error in errors)
        raise ValueError(error_message)
    
    return True

# Run validation on import if not in debug mode
if not settings.DEBUG:
    # Comment out for initial setup, uncomment for production
    pass  # validate_settings()