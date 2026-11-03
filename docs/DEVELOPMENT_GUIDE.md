# SchemaGenius AI - Development Guide

This guide provides detailed instructions for setting up, developing, and troubleshooting SchemaGenius AI.

## Table of Contents
- [Initial Setup](#initial-setup)
- [Development Workflow](#development-workflow)
- [Code Organization](#code-organization)
- [Common Tasks](#common-tasks)
- [Debugging](#debugging)
- [Troubleshooting](#troubleshooting)

---

## Initial Setup

### 1. Prerequisites Installation

#### Windows Setup

**Node.js and npm:**
```bash
# Download from https://nodejs.org/
# Choose LTS version (18.x or 20.x)
# During installation, check "Add to PATH"

# Verify installation
node --version  # Should show v18.x.x or v20.x.x
npm --version   # Should show 9.x.x or higher
```

**Python:**
```bash
# Download from https://python.org/downloads/
# Choose Python 3.11 or 3.12
# IMPORTANT: Check "Add Python to PATH" during installation

# Verify installation
python --version  # Should show Python 3.11.x or 3.12.x
pip --version     # Should show pip 23.x or higher
```

**Docker Desktop:**
```bash
# Download from https://www.docker.com/products/docker-desktop/
# Install and start Docker Desktop
# Enable WSL 2 backend if prompted

# Verify installation
docker --version
docker-compose --version
```

### 2. Clone and Setup Project

```bash
# Navigate to project directory
cd C:\Users\admin\Desktop\vallox

# Check Git status
git status
```

### 3. Start PostgreSQL Databases

```bash
# Start both application and sandbox databases
docker-compose up -d

# Verify containers are running
docker ps
# You should see:
# - schemagenuis_postgres (port 5432)
# - schemagenuis_sandbox (port 5433)

# Check logs if needed
docker-compose logs postgres
docker-compose logs postgres_sandbox

# Stop containers when done
docker-compose down
```

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows Command Prompt:
venv\Scripts\activate.bat
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Git Bash:
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Copy environment template
copy .env.example .env

# Edit .env file with your credentials
notepad .env
```

**Required environment variables:**
```env
# Leave these as-is for local development
DATABASE_URL=postgresql://schemagenuis_user:schemagenuis_dev_password@localhost:5432/schemagenuis_db
SANDBOX_DATABASE_URL=postgresql://sandbox_user:sandbox_dev_password@localhost:5433/sandbox_db

# Add your Gemini API key
GEMINI_API_KEY=your-key-from-google-ai-studio

# Will configure in MILESTONE 3
FIREBASE_CREDENTIALS_PATH=
```

### 5. Frontend Setup

```bash
cd ..\frontend  # or cd ../frontend in Git Bash

# Install dependencies
npm install

# Copy environment template
copy .env.example .env

# Edit .env file
notepad .env
```

**Required environment variables:**
```env
# Leave this as-is for local development
VITE_API_URL=http://localhost:8000

# Will configure in MILESTONE 3
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
```

---

## Development Workflow

### Starting Development Servers

You need **THREE terminal windows**:

**Terminal 1 - Docker (PostgreSQL):**
```bash
cd C:\Users\admin\Desktop\vallox
docker-compose up
# Leave this running
```

**Terminal 2 - Backend:**
```bash
cd C:\Users\admin\Desktop\vallox\backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Leave this running
```

**Terminal 3 - Frontend:**
```bash
cd C:\Users\admin\Desktop\vallox\frontend
npm run dev
# Leave this running
```

### Verifying Everything Works

1. **Frontend**: Open http://localhost:5173
   - Should see SchemaGenius AI landing page
   - Counter button should work

2. **Backend API**: Open http://localhost:8000/health
   - Should see: `{"status":"healthy","app_name":"SchemaGenius AI",...}`

3. **API Docs**: Open http://localhost:8000/api/docs
   - Should see Swagger UI with interactive API documentation

4. **Database**: Check containers
   ```bash
   docker ps
   # Should show both containers with "Up" status
   ```

---

## Code Organization

### Backend Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings and configuration
│   ├── dependencies.py      # Shared dependencies
│   │
│   ├── core/                # Core functionality
│   │   ├── security.py      # Authentication helpers
│   │   ├── database.py      # Database session management
│   │   └── exceptions.py    # Custom exception classes
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── project.py
│   │   └── schema_version.py
│   │
│   ├── schemas/             # Pydantic request/response models
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── schema.py        # Canonical schema definition
│   │   └── validation.py
│   │
│   ├── api/                 # API routes
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── projects.py
│   │       ├── generation.py
│   │       ├── schemas.py
│   │       ├── validation.py
│   │       ├── sql.py
│   │       └── sandbox.py
│   │
│   ├── services/            # Business logic
│   │   ├── gemini_service.py
│   │   ├── schema_validator.py
│   │   ├── sql_generator.py
│   │   └── sandbox_service.py
│   │
│   └── repositories/        # Data access layer
│       ├── user_repository.py
│       ├── project_repository.py
│       └── schema_repository.py
│
└── tests/
    ├── test_auth.py
    ├── test_validation.py
    └── test_sql_generation.py
```

### Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx             # React entry point
│   ├── App.tsx              # Root component
│   ├── index.css            # Global styles
│   │
│   ├── components/
│   │   ├── ui/              # shadcn/ui base components
│   │   ├── layout/          # Layout components
│   │   ├── auth/            # Authentication components
│   │   ├── schema/          # Schema editing components
│   │   └── common/          # Shared components
│   │
│   ├── pages/               # Page components
│   │   ├── LandingPage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── WorkspacePage.tsx
│   │
│   ├── features/            # Feature modules
│   │   ├── auth/
│   │   ├── projects/
│   │   └── schema/
│   │
│   ├── services/            # API clients
│   │   ├── api.ts
│   │   ├── authService.ts
│   │   └── schemaService.ts
│   │
│   ├── types/               # TypeScript types
│   │   ├── schema.ts
│   │   └── user.ts
│   │
│   └── lib/                 # Utilities
│       └── utils.ts
│
└── public/
    └── favicon.ico
```

---

## Common Tasks

### Adding a New Backend Dependency

```bash
cd backend
venv\Scripts\activate

# Install package
pip install package-name

# Update requirements
pip freeze > requirements.txt
```

### Adding a New Frontend Dependency

```bash
cd frontend

# Install package
npm install package-name

# Update package-lock.json automatically
```

### Creating a Database Migration

```bash
cd backend
venv\Scripts\activate

# After modifying SQLAlchemy models:
alembic revision --autogenerate -m "Description of changes"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Running Tests

```bash
# Backend tests
cd backend
venv\Scripts\activate
pytest

# Run specific test file
pytest tests/test_validation.py

# Run with coverage
pytest --cov=app --cov-report=html
```

### Code Formatting

```bash
# Backend (Black)
cd backend
black .

# Check without modifying
black --check .

# Frontend (Prettier - when added)
cd frontend
npm run lint
```

### Checking Type Safety

```bash
# Backend (mypy)
cd backend
mypy app/

# Frontend (TypeScript)
cd frontend
npm run build  # TypeScript errors will show
```

---

## Debugging

### Backend Debugging in VS Code

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true,
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    }
  ]
}
```

Set breakpoints in Python code and press F5 to start debugging.

### Frontend Debugging

1. Open Developer Tools (F12) in browser
2. Use React DevTools extension
3. Check Network tab for API calls
4. View Console for errors

### Database Debugging

```bash
# Connect to application database
docker exec -it schemagenuis_postgres psql -U schemagenuis_user -d schemagenuis_db

# Connect to sandbox database
docker exec -it schemagenuis_sandbox psql -U sandbox_user -d sandbox_db

# Common psql commands:
\dt                # List tables
\d table_name      # Describe table
SELECT * FROM users LIMIT 10;
\q                 # Quit
```

### API Debugging

Use the built-in Swagger UI:
1. Open http://localhost:8000/api/docs
2. Click on an endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

---

## Troubleshooting

### Docker Issues

**Problem**: `docker-compose up` fails with "port already in use"

**Solution**:
```bash
# Find process using port 5432
netstat -ano | findstr :5432

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different ports in docker-compose.yml
```

**Problem**: Container starts but health check fails

**Solution**:
```bash
# Check container logs
docker-compose logs postgres

# Restart containers
docker-compose down
docker-compose up -d
```

### Backend Issues

**Problem**: `ModuleNotFoundError` when running backend

**Solution**:
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**Problem**: Database connection error

**Solution**:
1. Verify Docker containers are running: `docker ps`
2. Check DATABASE_URL in `.env`
3. Test connection:
   ```bash
   docker exec -it schemagenuis_postgres psql -U schemagenuis_user -d schemagenuis_db
   ```

**Problem**: `pydantic-settings` import error

**Solution**:
```bash
pip install --upgrade pydantic pydantic-settings
```

### Frontend Issues

**Problem**: `npm install` fails

**Solution**:
```bash
# Delete node_modules and try again
rmdir /s node_modules
npm install

# If still fails, clear npm cache
npm cache clean --force
npm install
```

**Problem**: Vite dev server won't start

**Solution**:
```bash
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Use different port
npm run dev -- --port 3000
```

**Problem**: TypeScript errors in IDE but code runs

**Solution**:
```bash
# Restart TypeScript server in VS Code
# Press Ctrl+Shift+P → "TypeScript: Restart TS Server"

# Or rebuild
npm run build
```

**Problem**: Tailwind styles not applying

**Solution**:
1. Check `tailwind.config.js` has correct content paths
2. Verify `postcss.config.js` exists
3. Restart dev server
4. Clear browser cache

### CORS Issues

**Problem**: Frontend can't reach backend API

**Solution**:
1. Check backend is running: http://localhost:8000/health
2. Verify `ALLOWED_ORIGINS` in backend `.env`
3. Check `VITE_API_URL` in frontend `.env`
4. Look for CORS errors in browser console

### Git Issues

**Problem**: Large files rejected by GitHub

**Solution**:
```bash
# Check .gitignore includes:
node_modules/
venv/
*.db
.env
```

**Problem**: Merge conflicts

**Solution**:
```bash
# See conflicted files
git status

# Edit files to resolve conflicts
# Look for <<<<<<< HEAD markers

# After resolving
git add .
git commit
```

---

## Best Practices

### Python Code Style

- Use Black for formatting (line length 88)
- Use type hints for function parameters and returns
- Write docstrings for all public functions
- Keep functions small and focused
- Use Pydantic models for data validation

### TypeScript Code Style

- Use functional components with hooks
- Extract reusable logic into custom hooks
- Use TypeScript types, avoid `any`
- Keep components small and focused
- Use meaningful variable names

### Git Workflow

```bash
# Before starting work
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit frequently
git add .
git commit -m "Clear description of changes"

# Push to GitHub
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Testing

- Write tests before fixing bugs (TDD approach)
- Test edge cases and error conditions
- Mock external services (Firebase, Gemini)
- Keep tests independent and isolated
- Use meaningful test names

---

## Useful Commands Reference

### Docker
```bash
docker-compose up -d          # Start in background
docker-compose down           # Stop and remove
docker-compose ps             # List containers
docker-compose logs -f        # Follow logs
docker-compose restart        # Restart services
```

### Backend
```bash
uvicorn app.main:app --reload # Start dev server
pytest                        # Run tests
black .                       # Format code
mypy app/                     # Type checking
alembic upgrade head          # Apply migrations
```

### Frontend
```bash
npm run dev                   # Start dev server
npm run build                 # Build for production
npm run preview               # Preview production build
npm run lint                  # Lint code
```

---

**Last Updated**: 2026-11-03  
**Maintained by**: SchemaGenius AI Development Team
