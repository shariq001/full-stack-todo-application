# Quickstart Guide: Backend Infrastructure & Data Layer Setup

**Feature**: Backend Infrastructure & Data Layer Setup
**Date**: 2026-02-02
**Version**: 1.0

## Overview

This guide provides step-by-step instructions to set up the backend infrastructure for the todo application, including FastAPI server initialization, Neon PostgreSQL database connection, and core data schemas for User and Task entities.

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Access to Neon Serverless PostgreSQL instance
- Git for version control

## Environment Setup

1. **Clone the repository** (if starting fresh):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi sqlmodel python-dotenv uvicorn psycopg2-binary pytest
   ```

## Configuration

1. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Update environment variables** in `.env`:
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   ENVIRONMENT=development
   DEBUG=True
   ```

## Database Setup

1. **Initialize the database connection**:
   The application will automatically create the necessary tables when started.

2. **Verify database connection**:
   ```bash
   python -c "from backend.src.models.base import engine; print('Database connection successful')"
   ```

## Running the Application

1. **Start the development server**:
   ```bash
   uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Testing

1. **Run database connection tests**:
   ```bash
   pytest tests/test_database.py
   ```

2. **Run all tests**:
   ```bash
   pytest
   ```

## Key Components

### Models
- `backend/src/models/user.py` - User data model
- `backend/src/models/task.py` - Task data model
- `backend/src/models/base.py` - Database base class and engine

### Services
- `backend/src/services/database.py` - Database connection management

### API Endpoints
- `backend/src/api/health.py` - Health check endpoint

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify DATABASE_URL in .env is correct
   - Check that Neon PostgreSQL is accessible
   - Ensure SSL settings are properly configured

2. **Environment Variables Not Loading**:
   - Confirm .env file exists and is in the correct location
   - Verify python-dotenv is installed and working

3. **Migration Issues**:
   - Tables should be created automatically on first run
   - Check database permissions if tables aren't created

### Verification Commands

1. **Check if models are properly defined**:
   ```python
   from backend.src.models.user import User
   from backend.src.models.task import Task

   print("User model:", User.__tablename__)
   print("Task model:", Task.__tablename__)
   ```

2. **Test database connectivity**:
   ```python
   from backend.src.services.database import get_db
   import asyncio

   async def test_connection():
       async for db in get_db():
           print("Database connected successfully")
           break

   asyncio.run(test_connection())
   ```

## Next Steps

1. Implement authentication system using Better Auth
2. Create CRUD endpoints for Task management
3. Develop frontend interface to interact with the API
4. Add more sophisticated error handling and logging

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon Serverless PostgreSQL](https://neon.tech/docs/)