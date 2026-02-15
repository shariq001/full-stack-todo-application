"""FastAPI application entry point - imports from src.main for full functionality."""
from src.main import app

# HuggingFace expects 'app' variable
if __name__ == "__main__":
    import uvicorn
    import logging

    logging.info("Starting Uvicorn on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
