from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from app.models.response import BaseResponse
from app.api.deps import get_scraper

router = APIRouter()

@router.get("/nilai", response_model=BaseResponse)
async def get_nilai(
    session_id: str,
    semester: Optional[str] = Query(None, description="Semester (misal: 20241)"),
    scraper = Depends(lambda: get_scraper(session_id))
):
    """Get data nilai"""
    try:
        data = scraper.get_nilai(semester)
        return BaseResponse(
            status="success",
            message="Nilai berhasil diambil",
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )