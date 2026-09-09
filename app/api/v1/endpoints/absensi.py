from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from app.models.response import BaseResponse
from app.api.deps import get_scraper

router = APIRouter()

@router.get("/absensi", response_model=BaseResponse)
async def get_absensi(
    session_id: str,
    from_date: Optional[str] = Query(None, description="Tanggal mulai (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Tanggal akhir (YYYY-MM-DD)"),
    scraper = Depends(lambda: get_scraper(session_id))
):
    """Get data absensi"""
    try:
        data = scraper.get_absensi(from_date, to_date)
        return BaseResponse(
            status="success",
            message="Absensi berhasil diambil",
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )