# Data Model: Backend Infrastructure & Data Layer Setup

**Feature**: Backend Infrastructure & Data Layer Setup
**Date**: 2026-02-02
**Data Model Version**: 1.0

## Entity Definitions

### User Model
- **Table Name**: `users`
- **Description**: Represents system users with basic identification information

#### Fields:
- `id`: Primary key, UUID (or auto-incrementing integer)
  - Type: UUID (PostgreSQL) or Integer (with auto-increment)
  - Constraints: Primary Key, Not Null
  - Unique identifier for each user

- `email`: User's email address
  - Type: String (255 characters maximum)
  - Constraints: Not Null, Unique
  - Must be a valid email format

- `created_at`: Timestamp of record creation
  - Type: DateTime (with timezone)
  - Constraints: Not Null
  - Auto-populated with current timestamp on record creation

- `updated_at`: Timestamp of last record update
  - Type: DateTime (with timezone)
  - Constraints: Nullable
  - Auto-updated with current timestamp on record modification

### Task Model
- **Table Name**: `tasks`
- **Description**: Represents individual tasks associated with users

#### Fields:
- `id`: Primary key, UUID (or auto-incrementing integer)
  - Type: UUID (PostgreSQL) or Integer (with auto-increment)
  - Constraints: Primary Key, Not Null
  - Unique identifier for each task

- `title`: Task title or subject
  - Type: String (255 characters maximum)
  - Constraints: Not Null
  - Brief descriptive title of the task

- `description`: Detailed description of the task
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

## Relationships

### User → Task (One-to-Many)
- One User can have many Tasks
- Foreign Key: Task.user_id → User.id
- Cascade Behavior: TBD (likely restrict deletion of users with existing tasks)

## Database Constraints

### Primary Keys
- Both User and Task tables have auto-generated primary keys
- UUID approach preferred for distributed systems

### Unique Constraints
- User.email: Ensures no duplicate email addresses
- Prevents multiple accounts with the same email

### Foreign Key Constraints
- Task.user_id references User.id
- Ensures referential integrity between tasks and users
- Prevents orphaned task records

### Indexes
- Index on User.email for fast authentication lookups
- Index on Task.user_id for efficient querying by user
- Index on Task.is_completed for filtering completed/incomplete tasks

## Sample SQL Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
CREATE INDEX idx_users_email ON users(email);
```

## Validation Rules

### User Model
- Email format must conform to RFC 5322 standards
- Email must be unique across all users
- All required fields must be present during creation

### Task Model
- Title must be provided and not empty
- Task must be associated with a valid user
- is_completed field must be a boolean value

## Future Extensions
- Additional User fields (name, profile information) for enhanced user profiles
- Task categories or tags for better organization
- Priority levels for task management
- Due dates for time-sensitive tasks