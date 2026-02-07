# Data Model: Core API Development & Business Logic

**Feature**: Core API Development & Business Logic
**Date**: 2026-02-04
**Data Model Version**: 1.0

## Entity Definitions

### Task Model
- **Table Name**: `tasks`
- **Purpose**: Represents a user's individual task with all relevant information

#### Database Fields:
- `id`: Primary key identifier
  - Type: UUID (PostgreSQL) or Integer (with auto-increment)
  - Constraints: Primary Key, Not Null
  - Auto-generated unique identifier for the task

- `title`: Task title or subject
  - Type: String (255 characters maximum)
  - Constraints: Not Null
  - Brief descriptive title of the task

- `description`: Detailed task description
  - Type: Text (unlimited length)
  - Constraints: Nullable
  - Optional detailed description of the task requirements

- `is_completed`: Task completion status
  - Type: Boolean
  - Constraints: Not Null
  - Default: False
  - Indicates whether the task has been completed

- `user_id`: Foreign key to User
  - Type: UUID (matches User.id type) or Integer (matches User.id type)
  - Constraints: Not Null, Foreign Key (references users.id)
  - Associates the task with a specific user

- `created_at`: Timestamp of record creation
  - Type: DateTime (with timezone)
  - Constraints: Not Null
  - Auto-populated with current timestamp on record creation

- `updated_at`: Timestamp of last record update
  - Type: DateTime (with timezone)
  - Constraints: Nullable
  - Auto-updated with current timestamp on record modification

#### SQLModel Class Definition:
```python
class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(sa_column=Column(String, nullable=False))
    description: Optional[str] = Field(sa_column=Column(Text, nullable=True))
    is_completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default=None)
```

### Task Response Model
- **Purpose**: Structured response for API endpoints excluding sensitive information
- **Used for**: GET, POST, PUT responses

#### Response Fields:
- `id`: Task identifier
  - Type: UUID
  - Required: Yes
  - Unique identifier for the task

- `title`: Task title
  - Type: String
  - Required: Yes
  - Brief descriptive title of the task

- `description`: Task description
  - Type: String
  - Required: No
  - Optional detailed description of the task

- `is_completed`: Completion status
  - Type: Boolean
  - Required: Yes
  - Indicates whether the task has been completed

- `user_id`: Associated user identifier
  - Type: UUID
  - Required: Yes
  - Reference to the user who owns this task

- `created_at`: Creation timestamp
  - Type: DateTime (ISO 8601 format)
  - Required: Yes
  - When the task was originally created

- `updated_at`: Last update timestamp
  - Type: DateTime (ISO 8601 format) | null
  - Required: No
  - When the task was last modified

#### Pydantic Response Schema:
```python
class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    is_completed: bool
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
```

### Task Creation Model
- **Purpose**: Validation schema for creating new tasks
- **Used for**: POST /tasks request body

#### Input Fields:
- `title`: Task title
  - Type: String
  - Required: Yes
  - Maximum length: 255 characters
  - Cannot be empty

- `description`: Task description
  - Type: String
  - Required: No
  - Maximum length: unlimited
  - Can be null or empty

- `is_completed`: Initial completion status
  - Type: Boolean
  - Required: No
  - Default: False
  - Whether the task should be initially marked as completed

#### Pydantic Creation Schema:
```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: Optional[bool] = False
```

### Task Update Model
- **Purpose**: Validation schema for updating existing tasks
- **Used for**: PUT /tasks/{id} request body

#### Input Fields:
- `title`: Task title
  - Type: String
  - Required: No
  - Maximum length: 255 characters
  - When provided, updates the task title

- `description`: Task description
  - Type: String
  - Required: No
  - Maximum length: unlimited
  - When provided, updates the task description

- `is_completed`: Completion status
  - Type: Boolean
  - Required: No
  - When provided, updates the completion status

#### Pydantic Update Schema:
```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: Optional[bool] = None
```

## Relationship Models

### User → Task (One-to-Many)
- **Relationship**: One User can have many Tasks
- **Foreign Key**: Task.user_id → User.id
- **Constraint**: Cascade Behavior - Prevent deletion of users with existing tasks

## API Endpoint Specifications

### GET /tasks
- **Purpose**: Retrieve all tasks for the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Query**: `SELECT * FROM tasks WHERE user_id = :current_user_id ORDER BY created_at DESC`
- **Response**: Array of TaskResponse objects
- **Status Codes**: 200 (success), 401 (unauthorized)

### POST /tasks
- **Purpose**: Create a new task for the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Request Body**: TaskCreate object
- **Logic**: Set task.user_id to current_user.id before saving
- **Response**: Created TaskResponse object
- **Status Codes**: 201 (created), 401 (unauthorized), 422 (validation error)

### PUT /tasks/{id}
- **Purpose**: Update an existing task for the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Path Parameter**: id (UUID) - task identifier
- **Request Body**: TaskUpdate object
- **Query**: `SELECT * FROM tasks WHERE id = :task_id AND user_id = :current_user_id`
- **Validation**: Task must exist and be owned by current user
- **Response**: Updated TaskResponse object
- **Status Codes**: 200 (success), 401 (unauthorized), 404 (not found), 422 (validation error)

### DELETE /tasks/{id}
- **Purpose**: Delete an existing task for the authenticated user
- **Authentication**: Required via `current_user` dependency
- **Path Parameter**: id (UUID) - task identifier
- **Query**: `DELETE FROM tasks WHERE id = :task_id AND user_id = :current_user_id`
- **Validation**: Task must exist and be owned by current user
- **Response**: Empty response body
- **Status Codes**: 204 (deleted), 401 (unauthorized), 404 (not found)

## Data Isolation Mechanisms

### Query Filtering
- All queries that access tasks must include the filter: `WHERE user_id = :current_user_id`
- This ensures users can only see their own tasks
- Implementation pattern: `select(Task).where(Task.user_id == current_user.id)`

### Authentication Enforcement
- Every route handler must accept the `current_user` dependency
- Route functions must use current_user.id for filtering
- Unauthorized requests must return 401 status code

### Ownership Validation
- Before updating or deleting a task, verify the user owns it
- If a user attempts to access another user's task, return 404 (not found)
- Never reveal that a resource exists if the user doesn't have access to it

## Validation Rules

### Task Creation Validation
- Title is required and must be between 1-255 characters
- Description can be null or any length
- is_completed defaults to false if not provided

### Task Update Validation
- Title must be between 1-255 characters if provided
- Description can be null or any length if provided
- Only fields provided in request body are updated

### Task Deletion Validation
- Only allow deletion of tasks owned by current user
- If task doesn't exist or isn't owned by user, return 404

## Database Constraints

### Primary Keys
- Task.id must be unique and not null
- Auto-generated UUID for distributed system compatibility

### Foreign Keys
- Task.user_id must reference a valid User.id
- Prevents orphaned task records
- Maintains referential integrity

### Indexes
- Index on Task.user_id for efficient filtering
- Index on Task.created_at for chronological sorting
- Index on Task.is_completed for filtering by completion status