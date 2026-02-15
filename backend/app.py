"""Entry point for HuggingFace Spaces."""
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

logger.info("Starting FastAPI app initialization...")

try:
    # Import the FastAPI app
    from src.main import app
    logger.info("FastAPI app imported successfully")
except Exception as e:
    logger.error(f"Failed to import FastAPI app: {str(e)}", exc_info=True)
    raise

# HuggingFace Spaces will look for 'app' variable
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server on 0.0.0.0:7860")
    uvicorn.run(app, host="0.0.0.0", port=7860, log_level="info")
