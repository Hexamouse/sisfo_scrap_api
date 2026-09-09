import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
    # SISFO Config
    SISFO_BASE_URL: str = os.getenv('SISFO_BASE_URL', 'https://sisfo.upiyptk.ac.id')
    SISFO_USERNAME: str = os.getenv('SISFO_USERNAME', '22101152630449')
    SISFO_PASSWORD: str = os.getenv('SISFO_PASSWORD', '2213669NA')
    
    # Server Config
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 8000))
    RELOAD: bool = os.getenv('RELOAD', 'True').lower() == 'true'
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-here')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'DEBUG')  # Set DEBUG untuk troubleshooting

settings = Settings()