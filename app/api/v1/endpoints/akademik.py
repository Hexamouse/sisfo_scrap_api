from fastapi import APIRouter, HTTPException, status, Depends
from app.models.response import BaseResponse
from app.api.deps import get_scraper

router = APIRouter()

@router.get("/info-akademik", response_model=BaseResponse)
async def get_info_akademik(
    session_id: str,
    scraper = Depends(lambda: get_scraper(session_id))
):
    """Get info akademik"""
    try:
        data = scraper.get_info_akademik()
        return BaseResponse(
            status="success",
            message="Info akademik berhasil diambil",
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )