from fastapi import HTTPException, status
from typing import Dict
from app.core.scraper import SISFOScraper

# Simpan session scraper per user (simple in-memory)
# Untuk production, pake Redis atau database
scraper_sessions: Dict[str, SISFOScraper] = {}

def get_scraper(session_id: str) -> SISFOScraper:
    """Get scraper instance for a session"""
    if session_id not in scraper_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found. Please login first."
        )
    return scraper_sessions[session_id]

def create_scraper(base_url: str) -> SISFOScraper:
    """Create new scraper instance"""
    return SISFOScraper(base_url)