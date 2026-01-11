# CLI Todo App

A console-based todo application with in-memory storage built with Python.

## Features

- Add new tasks with title and description
- View all tasks with their status
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- In-memory storage (data persists only during runtime)

## Requirements

- Python 3.13+
- UV package manager (optional, for dependency management)

## Quick Start

### Method 1: Direct Python execution
```bash
python run_todo_app.py
```

### Method 2: From src directory
```bash
cd src
python main.py
```

## Usage

The application provides a menu-driven interface:

1. **Add a new task** - Create tasks with title and optional description
2. **View all tasks** - Display all tasks with ID, status, title, and description
3. **Update a task** - Modify existing task title or description
4. **Delete a task** - Remove tasks by ID (with confirmation)
5. **Mark task as complete** - Update task status to completed
6. **Mark task as incomplete** - Update task status to pending
7. **Exit** - Quit the application

## Architecture

The application follows a Model-View-Controller (MVC) pattern:

- **Models** (`src/models/`): Task data model
- **Services** (`src/services/`): Business logic (TaskManager)
- **UI** (`src/ui/`): Command-line interface
- **Main** (`src/main.py`): Application entry point

## Project Structure

```
src/
├── models/
│   └── task.py          # Task data model
├── services/
│   └── manager.py       # Task management business logic
├── ui/
│   └── cli.py           # CLI interface and menu system
├── main.py              # Application entry point
└── run_todo_app.py      # Alternative entry point (from project root)
```

## Development

The project was built using Spec-Driven Development methodology with the following phases:

1. **Specification**: Defined user stories and requirements
2. **Planning**: Architectural design and component breakdown
3. **Tasking**: Detailed implementation tasks organized by user story
4. **Implementation**: Built following the task breakdown

All 5 core user stories have been implemented:
- P1: Add New Tasks
- P1: View All Tasks
- P2: Update Task Details
- P2: Delete Tasks
- P2: Mark Tasks Complete/Incomplete"# In-Memory-Todo-List-App" 
"# In-Memory-Todo-List-App" 
"# In-Memory-Todo-List-App" 
