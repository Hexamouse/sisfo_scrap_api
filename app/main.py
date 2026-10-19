from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as api_v1_router
from app.core.config import settings
import logging

# Setup logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SISFO Scraper API",
    description="API untuk scraping data akademik dari SISFO",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_v1_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "SISFO Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": {
                "login": "POST /api/v1/auth/login",
                "logout": "POST /api/v1/auth/logout"
            },
            "sisfo": {
                "dashboard": "GET /api/v1/sisfo/dashboard?session_id={session_id}",
                "jadwal": "GET /api/v1/sisfo/jadwal?session_id={session_id}&semester={semester}",
                "nilai": "GET /api/v1/sisfo/nilai?session_id={session_id}&semester={semester}",
                "absensi": "GET /api/v1/sisfo/absensi?session_id={session_id}&from_date={date}&to_date={date}",
                "krs": "GET /api/v1/sisfo/krs?session_id={session_id}&semester={semester}",
                "transkrip": "GET /api/v1/sisfo/transkrip?session_id={session_id}",
                "info-akademik": "GET /api/v1/sisfo/info-akademik?session_id={session_id}",
                "biaya": "GET /api/v1/sisfo/biaya?session_id={session_id}"
            }
        }
    }

@app.on_event("startup")
async def startup():
    logger.info("Starting SISFO Scraper API")
    logger.info(f"Docs: http://localhost:{settings.PORT}/docs")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down SISFO Scraper API")
