"""Database service module for connection management."""
from sqlmodel import Session
from typing import Generator
from ..models.base import engine, create_db_and_tables
import logging

logger = logging.getLogger(__name__)
_db_initialized = False

def get_db_session() -> Generator[Session, None, None]:
    """Dependency to get database session for FastAPI."""
    global _db_initialized

    # Initialize tables on first use (lazy initialization)
    if not _db_initialized:
        try:
            logger.info("Lazy initializing database tables on first request...")
            create_db_and_tables()
            _db_initialized = True
            logger.info("Database tables initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}", exc_info=True)
            # Continue anyway - tables might already exist

    with Session(engine) as session:
        yield session


class DatabaseService:
    """Database service for connection management and operations."""

    def __init__(self):
        self.engine = engine

    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session."""
        with Session(self.engine) as session:
            yield session

    def initialize_tables(self):
        """Initialize database tables."""
        from ..models.base import create_db_and_tables
        create_db_and_tables()

    def close_engine(self):
        """Close the database engine."""
        self.engine.dispose()


db_service = DatabaseService()
