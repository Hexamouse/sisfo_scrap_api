from fastapi import APIRouter, HTTPException, status, Depends
from app.models.response import BaseResponse
from app.api.deps import get_scraper

router = APIRouter()

@router.get("/biaya", response_model=BaseResponse)
async def get_biaya(
    session_id: str,
    scraper = Depends(lambda: get_scraper(session_id))
):
    """Get biaya kuliah"""
    try:
        data = scraper.get_biaya()
        return BaseResponse(
            status="success",
            message="Biaya kuliah berhasil diambil",
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )