# Quickstart Guide: Core API Development & Business Logic

**Feature**: Core API Development & Business Logic
**Date**: 2026-02-04
**Version**: 1.0

## Overview

This guide provides step-by-step instructions to implement the core API endpoints for task management with strict user isolation. The API enforces authentication and ensures users can only access their own tasks.

## Prerequisites

- Python 3.10+ with pip
- Access to Neon Serverless PostgreSQL
- Completed authentication infrastructure (from previous spec)
- FastAPI and SQLModel dependencies installed

## Environment Setup

1. **Verify backend dependencies are installed**:
   ```bash
   pip install fastapi sqlmodel python-jose[cryptography] python-dotenv pytest
   ```

2. **Ensure authentication infrastructure is available**:
   - Verify `get_current_user` dependency exists in `backend/src/auth/dependencies.py`
   - Confirm `BETTER_AUTH_SECRET` is configured in environment

## Implementation Steps

### 1. Update Task Model

Update `backend/src/models/task.py` to include the complete Task model with relationships:

```python
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, Text
from uuid import uuid4
from datetime import datetime
from typing import Optional
import enum
from pydantic import BaseModel

class TaskBase(SQLModel):
    title: str = Field(sa_column=Column(String, nullable=False))
    description: Optional[str] = Field(sa_column=Column(Text, nullable=True))
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(nullable=False)  # Will reference User.id
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default=None)

# Response models
class TaskResponse(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
```

### 2. Create Task Service

Create `backend/src/services/task_service.py`:

```python
from sqlmodel import select, Session
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from uuid import UUID

def get_user_tasks(session: Session, user_id: str) -> List[Task]:
    """Retrieve all tasks for a specific user"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

def create_task(session: Session, task: TaskCreate, user_id: str) -> Task:
    """Create a new task for a specific user"""
    db_task = Task.from_orm(task)
    db_task.user_id = user_id
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Retrieve a specific task if it belongs to the user"""
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    task = session.exec(statement).first()
    return task

def update_task(session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update a specific task if it belongs to the user"""
    db_task = get_task_by_id_and_user(session, task_id, user_id)
    if not db_task:
        return None

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """Delete a specific task if it belongs to the user"""
    db_task = get_task_by_id_and_user(session, task_id, user_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True
```

### 3. Create Task API Endpoints

Create `backend/src/api/tasks.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlmodel import Session
from ..services.database import get_session
from ..auth.dependencies import get_current_user
from ..models.task import TaskResponse, TaskCreate, TaskUpdate
from ..services.task_service import (
    get_user_tasks,
    create_task,
    get_task_by_id_and_user,
    update_task,
    delete_task
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the authenticated user"""
    tasks = get_user_tasks(session, current_user['user_id'])
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_create: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user"""
    task = create_task(session, task_create, current_user['user_id'])
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a task owned by the authenticated user"""
    task = update_task(session, task_id, task_update, current_user['user_id'])
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task owned by the authenticated user"""
    deleted = delete_task(session, task_id, current_user['user_id'])
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return
```

### 4. Register Task Routes

Update `backend/src/api/main.py` to include the task routes:

```python
from fastapi import FastAPI
from .tasks import router as tasks_router
from .health import router as health_router

app = FastAPI(title="Todo API")

# Include routers
app.include_router(health_router)
app.include_router(tasks_router)
```

## Testing the API

### 1. Start the Development Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test with Valid Token

```bash
# Get all tasks for user
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer your-valid-jwt-token-here"

# Create a new task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-valid-jwt-token-here" \
  -d '{"title": "New Task", "description": "Task description", "is_completed": false}'

# Update a task
curl -X PUT http://localhost:8000/tasks/task-id-here \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-valid-jwt-token-here" \
  -d '{"title": "Updated Task Title", "is_completed": true}'

# Delete a task
curl -X DELETE http://localhost:8000/tasks/task-id-here \
  -H "Authorization: Bearer your-valid-jwt-token-here"
```

### 3. Test Data Isolation

```bash
# Attempt to access another user's task (should return 404)
curl -X GET http://localhost:8000/tasks/someone-elses-task-id \
  -H "Authorization: Bearer valid-token-for-different-user"
# Expected response: 404 Not Found
```

## Unit Testing

### 1. Create Task Tests

Create `backend/tests/test_tasks.py`:

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

def test_get_tasks_authenticated():
    """Test retrieving tasks with valid authentication"""
    with patch('src.api.deps.get_current_user') as mock_auth:
        mock_auth.return_value = {'user_id': 'user-123'}

        response = client.get("/tasks/", headers={"Authorization": "Bearer fake-token"})
        assert response.status_code == 200

def test_create_task_authenticated():
    """Test creating task with valid authentication"""
    with patch('src.api.deps.get_current_user') as mock_auth:
        mock_auth.return_value = {'user_id': 'user-123'}

        task_data = {"title": "Test Task", "description": "Test description"}
        response = client.post("/tasks/", json=task_data, headers={"Authorization": "Bearer fake-token"})
        assert response.status_code == 201

def test_access_other_user_task_returns_404():
    """Test that accessing another user's task returns 404"""
    with patch('src.api.deps.get_current_user') as mock_auth:
        # Mock user with ID 'user-123' trying to access a task that belongs to 'user-456'
        mock_auth.return_value = {'user_id': 'user-123'}

        response = client.get("/tasks/some-other-users-task-id", headers={"Authorization": "Bearer fake-token"})
        assert response.status_code == 404

def test_unauthenticated_access():
    """Test that unauthenticated requests return 401"""
    response = client.get("/tasks/")
    assert response.status_code == 401
```

## Key Components

### API Components
- `backend/src/api/tasks.py` - Task CRUD endpoints with authentication
- `backend/src/services/task_service.py` - Business logic for task operations
- `backend/src/models/task.py` - Task data models with validation

### Security Components
- Authentication dependency injection in all endpoints
- Data isolation through user_id filtering in queries
- Proper error handling (401 for auth, 404 for missing/foreign resources)

## Verification Commands

### 1. Verify Data Isolation Works

```bash
# This test ensures User A cannot access User B's data
pytest tests/test_tasks.py::test_access_other_user_task_returns_404 -v
```

### 2. Check API Documentation

- Visit http://localhost:8000/docs to verify API endpoints are documented
- Confirm all task endpoints show up in the Swagger interface
- Verify request/response models are properly defined

### 3. Test Error Conditions

```bash
# Test unauthorized access
curl -v -X GET http://localhost:8000/tasks
# Should return 401 Unauthorized

# Test non-existent task access
curl -v -X GET http://localhost:8000/tasks/non-existent-id \
  -H "Authorization: Bearer valid-token"
# Should return 404 Not Found
```

## Troubleshooting

### Common Issues

1. **404 Errors for Valid Tasks**:
   - Verify user_id filtering is correctly implemented
   - Confirm the task actually belongs to the authenticated user
   - Check that current_user.id is being properly passed to queries

2. **Authentication Errors**:
   - Verify JWT token is properly formatted (Bearer <token>)
   - Confirm `BETTER_AUTH_SECRET` is consistent across services
   - Check that authentication dependency is correctly injected

3. **Database Connection Issues**:
   - Verify database connection parameters in environment variables
   - Confirm SQLModel models are properly defined
   - Check that session management is working correctly

### Data Isolation Verification

```bash
# Manually test that User A cannot see User B's tasks
# 1. Authenticate as User A and create a task
# 2. Authenticate as User B and attempt to access User A's task ID
# 3. Should receive 404 Not Found (not 403 Forbidden - important for security)
```

## Next Steps

1. Implement frontend components to consume the task API
2. Add additional task features like filtering, sorting, and pagination
3. Enhance security with rate limiting and additional validation
4. Add comprehensive logging and monitoring
5. Deploy to staging environment for further testing

## Security Notes

- Always return 404 (Not Found) rather than 403 (Forbidden) when a user tries to access another user's resource
- Validate all input data to prevent injection attacks
- Use parameterized queries to prevent SQL injection
- Log security events appropriately
- Consider adding rate limiting to prevent abuse