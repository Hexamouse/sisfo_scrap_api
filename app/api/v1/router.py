from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, dashboard, jadwal, nilai, absensi, 
    krs, transkrip, akademik, biaya
)

router = APIRouter(prefix="/api/v1")

# Register semua endpoints
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(dashboard.router, prefix="/sisfo", tags=["Dashboard"])
router.include_router(jadwal.router, prefix="/sisfo", tags=["Jadwal"])
router.include_router(nilai.router, prefix="/sisfo", tags=["Nilai"])
router.include_router(absensi.router, prefix="/sisfo", tags=["Absensi"])
router.include_router(krs.router, prefix="/sisfo", tags=["KRS"])
router.include_router(transkrip.router, prefix="/sisfo", tags=["Transkrip"])
router.include_router(akademik.router, prefix="/sisfo", tags=["Akademik"])
router.include_router(biaya.router, prefix="/sisfo", tags=["Biaya"])