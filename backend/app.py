"""Minimal FastAPI app for HuggingFace Spaces."""
import logging
import os
import sys

# Setup logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=" * 50)
logger.info("APP STARTUP STARTING")
logger.info("=" * 50)

# Minimal FastAPI app without external imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger.info("FastAPI imported successfully")

# Create app
app = FastAPI(
    title="Todo Backend API",
    version="1.0.0"
)

logger.info("FastAPI app created")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS middleware added")

# Basic endpoints (no database)
@app.get("/")
async def root():
    """Root endpoint - no dependencies."""
    return {"status": "ok", "message": "Backend is running"}

@app.get("/health")
async def health():
    """Health check - no dependencies."""
    return {"status": "healthy"}

@app.get("/live")
async def live():
    """Liveness check - no dependencies."""
    return {"status": "alive"}

@app.get("/ready")
async def ready():
    """Readiness check - no dependencies."""
    return {"status": "ready"}

logger.info("=" * 50)
logger.info("APP STARTUP COMPLETE")
logger.info("=" * 50)
logger.info(f"App is ready to receive requests")

# HuggingFace expects 'app' variable
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn on 0.0.0.0:7860")
    uvicorn.run(app, host="0.0.0.0", port=7860)
