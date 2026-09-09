from fastapi import APIRouter, HTTPException, status, Depends
from app.models.response import BaseResponse
from app.api.deps import get_scraper

router = APIRouter()

@router.get("/transkrip", response_model=BaseResponse)
async def get_transkrip(
    session_id: str,
    scraper = Depends(lambda: get_scraper(session_id))
):
    """Get transkrip nilai"""
    try:
        data = scraper.get_transkrip()
        return BaseResponse(
            status="success",
            message="Transkrip berhasil diambil",
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )