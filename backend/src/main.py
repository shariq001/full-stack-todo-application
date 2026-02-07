"""Main FastAPI application."""
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .auth import get_current_user_from_token
from .models.base import create_db_and_tables
from .api.health import router as health_router
from .api.tasks import router as tasks_router
from .config.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler."""
    logging.info("Application starting up...")
    create_db_and_tables()
    logging.info("Database tables created/verified.")
    yield
    logging.info("Application shutting down...")


app = FastAPI(
    title="Backend Infrastructure API",
    description="API for the Backend Infrastructure & Data Layer Setup",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3002",
        "https://full-stack-todo-hazel.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(tasks_router)


@app.get("/me", response_model=dict)
async def read_current_user(authorization: str = Header(None)):
    """Get current authenticated user."""
    current_user = get_current_user_from_token(authorization)
    return {"user_id": current_user.id, "email": current_user.email}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Backend Infrastructure API is running!"}
