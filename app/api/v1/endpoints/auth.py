from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.models.request import LoginRequest
from app.models.response import AuthResponse
from app.api.deps import scraper_sessions
from app.core.config import settings
from app.core.scraper import SISFOScraper
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=AuthResponse)
async def login(login_data: LoginRequest):
    """
    Login ke SISFO
    
    Contoh request:
    {
        "username": "22101152630449",
        "password": "2213669NA"
    }
    """
    try:
        logger.info(f"Login attempt for: {login_data.username}")
        
        # Validasi input
        if not login_data.username or not login_data.password:
            logger.warning("Username atau password kosong")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username dan password tidak boleh kosong"
            )
        
        # Buat scraper instance langsung
        scraper = SISFOScraper(settings.SISFO_BASE_URL)
        
        # Login
        result = scraper.login(login_data.username, login_data.password)
        
        if not result.get('success'):
            logger.warning(f"Login failed for {login_data.username}: {result.get('message')}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result.get('message', 'Login gagal')
            )
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        scraper_sessions[session_id] = scraper
        
        logger.info(f"Login successful for {login_data.username}, session: {session_id[:8]}...")
        
        return AuthResponse(
            success=True,
            message="Login berhasil",
            token=session_id,
            user_data={
                'username': login_data.username,
                'session_id': session_id
            }
        )
        
    except HTTPException:
        raise
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/logout")
async def logout(session_id: str):
    """Logout dari SISFO"""
    try:
        if session_id in scraper_sessions:
            scraper = scraper_sessions[session_id]
            scraper.logout()
            del scraper_sessions[session_id]
            logger.info(f"Logout successful for session: {session_id[:8]}...")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success", 
                "message": "Logout berhasil"
            }
        )
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )