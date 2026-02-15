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
- PostgreSQL database (or Neon Serverless PostgreSQL recommended)

## Prerequisites Setup

Before running the application, you need to set up a database and get your connection credentials.

### Step 0: Set Up Your Database

We recommend **Neon Serverless PostgreSQL** for easy setup, but you can use any PostgreSQL provider.

#### Option A: Neon Serverless PostgreSQL (Recommended - 5 minutes)

1. **Create a Neon Account**
   - Visit: https://console.neon.tech/
   - Sign up with email or GitHub account

2. **Create a Project**
   - Click "New Project"
   - Name it something like "todo-app"
   - Choose your region (closest to you for best performance)
   - Click "Create"

3. **Get Your Connection String**
   - Once your project is created, you'll see the dashboard
   - Look for the "Connection String" section
   - Copy the "Connection string" that starts with `postgresql://`
   - It should look like: `postgresql://user:password@ep-xxxxx.us-east-1.aws.neon.tech/todo_app`

#### Option B: Local PostgreSQL

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - Follow the installation guide for your OS
   - Remember the password you set for the postgres user

2. **Create a Database**
   - Open PostgreSQL terminal (or pgAdmin)
   - Run: `CREATE DATABASE todo_app;`
   - Connection string: `postgresql://postgres:your_password@localhost:5432/todo_app`

#### Option C: Other Services
- **Railway**: https://railway.app/ (Copy connection string from dashboard)
- **Supabase**: https://supabase.com/ (PostgreSQL with extra features)
- **AWS RDS**: https://aws.amazon.com/rds/ (Production-grade)

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project directory
cd "Hackathon 2/Phase2"
```

### Step 2: Environment Configuration

This is the most important step. The application needs configuration files with your credentials.

1. **Copy the example environment file**
   ```bash
   # In the project root directory, copy .env.example to .env
   cp .env.example .env
   ```

2. **Edit the .env file with your database credentials**
   ```bash
   # Open .env in your text editor
   # Windows: use Notepad, VS Code, or your preferred editor
   ```

3. **Fill in the required values**

   **DATABASE_URL**: Paste your PostgreSQL connection string
   ```
   DATABASE_URL="postgresql://user:password@host/database_name"
   ```

   **BETTER_AUTH_SECRET**: Generate a random secret (at least 32 characters)

   To generate on your system:
   - **Linux/Mac**: `openssl rand -hex 32`
   - **Windows (PowerShell)**:
     ```powershell
     [Convert]::ToHexString((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
     ```
   - **Or** use: https://www.lastpass.com/features/generator

   Then paste it here (copy the entire output):
   ```
   BETTER_AUTH_SECRET="your_generated_secret_here"
   ```

4. **API Configuration** (leave as default for local development)
   ```
   NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
   NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
   ```

## Quick Start

### Option 1: CLI-Based Todo Application

Simple command-line interface - no database setup needed!

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

Complete web application with authentication and database persistence.

#### Step 1: Setup Backend (FastAPI)

Open Terminal/Command Prompt and run:

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn app:app --reload --port 8000
```

✅ Backend is ready when you see: `Application startup complete`
- Backend URL: `http://localhost:8000`

#### Step 2: Setup Frontend (Next.js)

Open a **NEW** Terminal/Command Prompt tab and run:

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

✅ Frontend is ready when you see: `compiled client and server successfully`
- Frontend URL: `http://localhost:3000`

#### Step 3: Access the Application

1. Open your browser
2. Go to: `http://localhost:3000`
3. Sign up with email and password
4. Start creating your todo items!

All your data will be saved to your PostgreSQL database.

## Troubleshooting

### Common Issues & Solutions

#### "ModuleNotFoundError: No module named '...'"
**Problem**: Backend won't start due to missing dependencies
**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

#### "DATABASE_URL cannot be empty"
**Problem**: Backend can't connect to database
**Solution**:
1. Check your `.env` file exists in the root directory
2. Verify `DATABASE_URL` is filled in correctly
3. Test the connection string format: `postgresql://user:password@host/database`
4. For Neon: Ensure URL includes the full connection string

#### "Cannot find module 'better-auth'"
**Problem**: Frontend missing dependencies
**Solution**:
```bash
cd frontend
npm install
```

#### "Error: connect ECONNREFUSED 127.0.0.1:8000"
**Problem**: Frontend can't reach the backend API
**Solution**:
1. Make sure backend is running: `python -m uvicorn app:app --reload --port 8000`
2. Check `NEXT_PUBLIC_API_BASE_URL` in `.env` is set to `http://localhost:8000`
3. Restart the frontend development server: `npm run dev`

#### "BETTER_AUTH_SECRET must be at least 32 characters long"
**Problem**: Authentication secret is too short
**Solution**:
1. Generate a new secret using the command mentioned in Setup Step 2
2. Copy the entire generated string (should be 64 hex characters for 32 bytes)
3. Update `BETTER_AUTH_SECRET` in `.env`

#### Port 3000 or 8000 already in use
**Problem**: Cannot start server - port is already in use
**Solution**:
```bash
# Use a different port
# For backend: python -m uvicorn app:app --port 8001
# For frontend: npm run dev -- -p 3001
```

#### Database Connection Timeout
**Problem**: "psycopg2.OperationalError: timeout expired"
**Solution**:
1. Check your internet connection
2. Verify the DATABASE_URL is correct
3. For Neon: Check that you're in the correct region
4. Wait a moment and try again (cold starts can take time)

### Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the error message carefully - it often contains the solution
3. Ensure all prerequisites are installed correctly
4. Try restarting the servers

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

### UI Version

After logging in, you can:
1. **Create Tasks** - Click "Add Task" and enter title/description
2. **View Tasks** - See all your tasks on the dashboard
3. **Update Tasks** - Click edit on any task to modify it
4. **Delete Tasks** - Click delete to remove a task
5. **Mark Complete** - Toggle completion status with checkboxes
6. **User Profile** - Manage your account settings
7. **Sign Out** - Log out when done

## Environment Variables Reference

### What Each Variable Does

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `BETTER_AUTH_SECRET` | JWT token secret (32+ chars) | Random hex string |
| `NEXT_PUBLIC_API_BASE_URL` | Frontend API endpoint | `http://localhost:8000` |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Frontend base URL for auth | `http://localhost:3000` |
| `ENVIRONMENT` | App environment mode | `development` or `production` |
| `DEBUG` | Enable debug mode | `true` or `false` |

### Environment Files Setup

The application uses environment variables in three ways:

1. **Root .env file** - Primary configuration
   - Location: `D:\Muhammad Shariq\GIAIC\Hackathon\Hackathon 2\Phase2\.env`
   - Created from: `.env.example`
   - Used by: Both backend and frontend

2. **Backend .env** (optional)
   - Location: `backend/.env`
   - Only needed if different settings from root
   - Automatically used by FastAPI

3. **Frontend .env** (optional)
   - Location: `frontend/.env.local` or `frontend/.env`
   - Only needed if different settings from root
   - Used by Next.js build process

## Architecture

The application follows a Model-View-Controller (MVC) pattern for CLI, and layered architecture for full-stack:

**CLI Version:**
- **Models** (`src/models/`): Task data model
- **Services** (`src/services/`): Business logic (TaskManager)
- **UI** (`src/ui/`): Command-line interface

**Full-Stack (UI) Version:**
- **Frontend** (Next.js): React components, authentication UI
- **Backend** (FastAPI): REST API endpoints, business logic
- **Database** (PostgreSQL): Persistent data storage
- **Authentication** (Better Auth): User signup/signin with JWT tokens

## Project Structure

```
.
├── .env.example              # Environment variables template
├── .env                      # Your actual configuration (created from .env.example)
├── README.md                 # This file
│
├── src/                      # CLI Application
│   ├── models/
│   │   └── task.py          # Task data model
│   ├── services/
│   │   └── manager.py       # Task management business logic
│   ├── ui/
│   │   └── cli.py           # CLI interface and menu system
│   └── main.py              # Application entry point
│
├── backend/                  # FastAPI Backend Server
│   ├── .env.example          # Backend environment template
│   ├── .env                  # Backend configuration
│   ├── requirements.txt      # Python dependencies
│   ├── src/
│   │   ├── config/
│   │   │   └── settings.py  # Settings loader
│   │   ├── models/
│   │   │   └── task.py      # Database models
│   │   ├── api/
│   │   │   └── tasks.py     # API routes
│   │   └── auth/
│   │       └── jwt.py       # JWT authentication
│   └── app.py               # FastAPI application
│
└── frontend/                 # Next.js Frontend
    ├── .env.example          # Frontend environment template
    ├── .env.local            # Frontend configuration
    ├── package.json          # JavaScript dependencies
    └── app/
        ├── page.tsx          # Home page
        ├── tasks/            # Task management pages
        └── auth/             # Authentication pages
```

## Getting Started Checklist

Use this checklist to ensure you're set up correctly:

- [ ] I have Node.js 18+ installed (`node --version`)
- [ ] I have Python 3.13+ installed (`python --version`)
- [ ] I created a PostgreSQL database (Neon or local)
- [ ] I have the database connection URL/string
- [ ] I copied `.env.example` to `.env` in the project root
- [ ] I filled in `DATABASE_URL` with my connection string
- [ ] I generated and filled in `BETTER_AUTH_SECRET` (32+ characters)
- [ ] I installed backend dependencies (`pip install -r requirements.txt`)
- [ ] I installed frontend dependencies (`npm install` in frontend folder)
- [ ] I can start the backend (`python -m uvicorn app:app --reload --port 8000`)
- [ ] I can start the frontend (`npm run dev` in frontend folder)
- [ ] I can access the app at `http://localhost:3000`
- [ ] I can sign up and create a task!

If any step fails, check the Troubleshooting section above.

## Credentials & Service Links

Here are the services and where to get your credentials:

| Service | Purpose | Link | Time to Set Up |
|---------|---------|------|-----------------|
| **Neon** | Database (Recommended) | https://console.neon.tech | 5 min |
| **PostgreSQL** | Database (Local) | https://www.postgresql.org | 15 min |
| **Node.js** | Frontend runtime | https://nodejs.org | 5 min |
| **Python** | Backend runtime | https://www.python.org | 5 min |

## Tips & Best Practices

### Development Tips
1. **Keep terminal windows open** - Have one for backend and one for frontend
2. **Watch for error messages** - They usually tell you exactly what's wrong
3. **Check .env file first** - Most errors are environment variable issues
4. **Clear browser cache** - If you see old data, try Ctrl+Shift+Delete (browser cache)

### Security Tips
1. **Never commit .env files** - These contain secrets!
2. **Use strong BETTER_AUTH_SECRET** - At least 32 characters
3. **Don't share your DATABASE_URL** - It contains your password
4. **Use different secrets for prod** - Never use dev secrets in production
5. **Regenerate secrets if leaked** - Security is important!

### Performance Tips
1. **For Neon users** - First request might be slow (cold start), subsequent ones are fast
2. **Use npm ci** instead of npm install - For reproducible builds
3. **Enable caching** in production - Set up Redis for better performance

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
- Multi-user support

### Important Note ⚠️

**✅ Local Development:** The application is **fully functional and working optimally** when run locally using the instructions provided above. This is the recommended way to run the application for development and testing.

**Production Deployment:** For deploying to production (cloud platforms, servers), additional configuration may be required. Contact the development team for production deployment guidelines. 
