# backend/app/core/config.py
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Settings:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "gcp-starter")  # Default to gcp-starter

    # WhatsApp Configuration
    WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    WHATSAPP_WEBHOOK_TOKEN = os.getenv("WHATSAPP_WEBHOOK_TOKEN", "carebuddy_webhook_token")

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./carebuddy.db")

    def __init__(self):
        # Validate required settings
        required_settings = [
            "OPENAI_API_KEY",
            "PINECONE_API_KEY",
            "WHATSAPP_ACCESS_TOKEN",
            "WHATSAPP_PHONE_NUMBER_ID"
        ]
        
        missing_settings = [
            setting for setting in required_settings 
            if not getattr(self, setting)
        ]
        
        if missing_settings:
            logger.error(f"Missing required environment variables: {', '.join(missing_settings)}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_settings)}")

settings = Settings()