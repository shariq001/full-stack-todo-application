# Data Model: CLI Todo App

## Task Entity

**Entity Name**: Task

**Fields**:
- `id`: Integer (Unique identifier for the task)
- `title`: String (Required title of the task)
- `description`: String (Optional description of the task)
- `completed`: Boolean (Status indicating if the task is completed)

**Validation Rules**:
- `id` must be a positive integer
- `title` must not be empty or None
- `completed` must be a boolean value (True/False)

**State Transitions**:
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user marks task as incomplete

**Relationships**:
- TaskList contains multiple Task entities
- Each Task belongs to exactly one TaskList

## TaskList Entity

**Entity Name**: TaskList

**Fields**:
- `tasks`: List of Task objects
- `next_id`: Integer (Counter for assigning unique IDs to new tasks)

**Methods**:
- `add_task(title: str, description: str)`: Creates a new Task and adds it to the list
- `remove_task(task_id: int)`: Removes a Task by ID
- `update_task(task_id: int, title: str, description: str)`: Updates a Task's properties
- `get_all_tasks()`: Returns all tasks in the list
- `mark_complete(task_id: int)`: Marks a Task as completed
- `mark_incomplete(task_id: int)`: Marks a Task as incomplete