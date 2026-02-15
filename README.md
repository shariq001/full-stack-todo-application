# Full-Stack Todo Application - Phase 2

A comprehensive todo application available in two versions: CLI-based (Python) and full-stack UI-based (Next.js + FastAPI).

## Features

- Add new tasks with title and description
- View all tasks with their status
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- User authentication (UI version)
- Persistent database storage with PostgreSQL (UI version)
- Multi-user support (UI version)

## Requirements

### CLI Version
- Python 3.13+
- UV package manager (optional, for dependency management)

### UI Version
- Node.js 18+ and npm
- Python 3.13+
- PostgreSQL database (or Neon Serverless PostgreSQL)

## Quick Start

### Option 1: CLI-Based Todo Application

#### Method 1: Direct Python execution
```bash
python run_todo_app.py
```

#### Method 2: From src directory
```bash
cd src
python main.py
```

### Option 2: UI-Based Todo Application (Full-Stack)

#### Step 1: Setup Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn app:app --reload --port 8000
```

The backend will be running on `http://localhost:8000`

#### Step 2: Setup Frontend (Next.js)
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be running on `http://localhost:3000`

#### Step 3: Access the Application
Open your browser and go to: `http://localhost:3000`

You can now:
- Sign up with a new account
- Sign in with your credentials
- Create, view, update, and delete todo items
- All data is saved to the database

## Usage

### CLI Version

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
- P2: Mark Tasks Complete/Incomplete

## Hackathon 2 - Phase 2

This is Phase 2 of Hackathon 2, expanding the Phase 1 CLI application into a complete full-stack solution with:
- User authentication system
- Database persistence
- Modern web-based UI
- RESTful API backend

### Important Note ⚠️

**Technical Issues in Deployment:** This phase currently has some deployment-related technical issues. The application is **fully functional and working optimally on the local environment**. For the best experience, please run both the CLI and UI versions locally using the instructions provided above.

For production deployment, additional configuration and troubleshooting may be required. 
