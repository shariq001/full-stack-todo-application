"""Health check endpoint."""
from fastapi import APIRouter, status
from typing import Dict
from sqlmodel import Session, text
from ..models.base import engine
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """Health check endpoint to verify the system is operational."""
    logger.info("Health check requested")
    try:
        # Try to connect to database with timeout
        import threading
        result = {"status": "healthy", "database": "unknown"}

        def check_db():
            try:
                with Session(engine) as session:
                    session.exec(text("SELECT 1"))
                result["database"] = "connected"
            except Exception as e:
                logger.error(f"DB check failed: {str(e)}")
                result["database"] = "disconnected"

        # Check DB in thread with timeout
        thread = threading.Thread(target=check_db, daemon=True)
        thread.start()
        thread.join(timeout=5)  # 5 second timeout

        logger.info(f"Health check: {result}")
        return result
    except Exception as e:
        logger.error(f"Health check error: {str(e)}", exc_info=True)
        return {"status": "healthy", "database": "unknown"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> Dict[str, str]:
    """Readiness check endpoint."""
    logger.info("Readiness check requested")
    return {"status": "ready"}


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """Liveness check endpoint."""
    logger.info("Liveness check requested")
    return {"status": "alive"}


@router.get("/debug", status_code=status.HTTP_200_OK)
async def debug_info() -> Dict:
    """Debug endpoint to check environment and configuration."""
    logger.info("Debug info requested")
    return {
        "status": "debug",
        "database_configured": bool(os.getenv("DATABASE_URL")),
        "auth_secret_configured": bool(os.getenv("BETTER_AUTH_SECRET")),
        "environment": os.getenv("ENVIRONMENT", "unknown")
    }
