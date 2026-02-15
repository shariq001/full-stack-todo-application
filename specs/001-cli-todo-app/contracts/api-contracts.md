# API Contracts: CLI Todo App

## Task Management Service Interface

### add_task(title: str, description: str) -> Task
- **Purpose**: Add a new task to the task list
- **Parameters**:
  - `title` (str): Required title of the task
  - `description` (str): Optional description of the task
- **Returns**: Task object with assigned ID and initial pending status
- **Errors**: ValueError if title is empty

### get_all_tasks() -> List[Task]
- **Purpose**: Retrieve all tasks in the task list
- **Parameters**: None
- **Returns**: List of all Task objects
- **Errors**: None

### update_task(task_id: int, title: str, description: str) -> bool
- **Purpose**: Update an existing task's information
- **Parameters**:
  - `task_id` (int): ID of the task to update
  - `title` (str): New title for the task
  - `description` (str): New description for the task
- **Returns**: True if successful, False if task ID not found
- **Errors**: None (returns False instead)

### remove_task(task_id: int) -> bool
- **Purpose**: Remove a task from the task list
- **Parameters**:
  - `task_id` (int): ID of the task to remove
- **Returns**: True if successful, False if task ID not found
- **Errors**: None (returns False instead)

### mark_complete(task_id: int) -> bool
- **Purpose**: Mark a task as completed
- **Parameters**:
  - `task_id` (int): ID of the task to mark complete
- **Returns**: True if successful, False if task ID not found
- **Errors**: None (returns False instead)

### mark_incomplete(task_id: int) -> bool
- **Purpose**: Mark a task as incomplete
- **Parameters**:
  - `task_id` (int): ID of the task to mark incomplete
- **Returns**: True if successful, False if task ID not found
- **Errors**: None (returns False instead)

## CLI Interface Contract

### display_menu() -> None
- **Purpose**: Display the main menu options to the user
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Prints menu to stdout

### capture_input(prompt: str) -> str
- **Purpose**: Capture user input with a prompt
- **Parameters**:
  - `prompt` (str): Message to display to user
- **Returns**: User input as string
- **Errors**: May raise exception on unexpected input issues

### render_task_list(tasks: List[Task]) -> None
- **Purpose**: Display tasks in a formatted way
- **Parameters**:
  - `tasks` (List[Task]): List of tasks to display
- **Returns**: None
- **Side Effects**: Prints task list to stdout