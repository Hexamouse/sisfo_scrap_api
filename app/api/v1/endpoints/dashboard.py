from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.response import BaseResponse
from app.api.deps import get_scraper
from app.core.scraper import SISFOScraper
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/dashboard", response_model=BaseResponse)
async def get_dashboard(
    session_id: str = Query(..., description="Session ID dari login"),
    scraper: SISFOScraper = Depends(get_scraper)
):
    """Get dashboard data"""
    try:
        data = scraper.get_dashboard()
        return BaseResponse(
            status="success",
            message="Dashboard berhasil diambil",
            data=data
        )
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )