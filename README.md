# SchemaGenius AI

**From Natural Language to Production-Ready Database Architecture**

An AI-powered database schema generation platform that converts natural-language requirements into structured database schemas with interactive ER diagrams.

## 🎯 Project Overview

SchemaGenius AI helps developers translate business requirements into professional database designs by:

- Converting natural language into database schemas using Google Gemini AI
- Generating interactive ER diagrams with React Flow
- Validating schemas with deterministic rule-based checks
- Generating production-ready SQL for MySQL and PostgreSQL
- Testing SQL in an isolated sandbox environment
- Managing schema versions and project history

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + Python 3.11+
- **Database**: PostgreSQL (Application) + PostgreSQL (Isolated Sandbox)
- **Authentication**: Firebase Authentication
- **AI**: Google Gemini API
- **Deployment**: Vercel (Frontend) + Render.com (Backend)

## 📋 Prerequisites

Before you begin, ensure you have installed:

- **Node.js** 18.x or 20.x LTS ([Download](https://nodejs.org/))
- **Python** 3.11 or 3.12 ([Download](https://www.python.org/downloads/))
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
- **Git** (already installed ✅)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
cd C:\Users\admin\Desktop\vallox
```

### 2. Start PostgreSQL with Docker

```bash
# Start both application and sandbox PostgreSQL instances
docker-compose up -d

# Verify containers are running
docker ps
```

You should see two containers:
- `schemagenuis_postgres` on port 5432
- `schemagenuis_sandbox` on port 5433

### 3. Backend Setup

```bash
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env and configure:
# - GEMINI_API_KEY (get from https://aistudio.google.com/app/apikey)
# - FIREBASE_CREDENTIALS_PATH (will configure in Milestone 3)
```

### 4. Frontend Setup

```bash
cd ..\frontend

# Install dependencies
npm install

# Copy environment template
copy .env.example .env

# Edit .env and configure:
# - VITE_API_URL=http://localhost:8000
# - Firebase config (will configure in Milestone 3)
```

### 5. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 6. Verify Installation

- **Frontend**: Open http://localhost:5173
  - You should see "SchemaGenius AI" with a working counter button
  
- **Backend API**: Open http://localhost:8000/health
  - You should see: `{"status":"healthy","app_name":"SchemaGenius AI",...}`
  
- **API Documentation**: Open http://localhost:8000/api/docs
  - Interactive Swagger UI for testing endpoints

## 📁 Project Structure

```
vallox/
├── frontend/              # React TypeScript frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── features/     # Feature modules
│   │   ├── services/     # API client services
│   │   ├── lib/          # Utilities
│   │   └── types/        # TypeScript types
│   └── package.json
│
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core functionality
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── main.py      # Application entry
│   ├── tests/           # Test suite
│   └── requirements.txt
│
├── docs/                # Documentation
├── docker-compose.yml   # PostgreSQL containers
└── README.md
```

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests (to be added in later milestones)
cd frontend
npm test
```

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Development Guide](docs/DEVELOPMENT_GUIDE.md)
- [API Documentation](docs/API.md)
- [Database Design](docs/DATABASE_DESIGN.md)
- [Security Guide](docs/SECURITY.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Progress Tracking](docs/PROGRESS.md)

## 🔒 Security

- Never commit `.env` files or Firebase service account keys
- Keep `GEMINI_API_KEY` server-side only
- Firebase tokens verified on every backend request
- SQL sandbox completely isolated from application database

## 🛠️ Common Issues

### Docker containers won't start
```bash
# Check if ports are already in use
netstat -ano | findstr :5432
netstat -ano | findstr :5433

# Stop and remove existing containers
docker-compose down
docker-compose up -d
```

### Python virtual environment issues
```bash
# Delete and recreate
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend build errors
```bash
# Clear node_modules and reinstall
rmdir /s node_modules
npm install
```

## 📝 Development Progress

Current Milestone: **MILESTONE 1 - PROJECT FOUNDATION** ✅

See [docs/PROGRESS.md](docs/PROGRESS.md) for detailed progress tracking.

## 🤝 Contributing

This is a portfolio project. For issues or suggestions, please open a GitHub issue.

## 📄 License

MIT License - feel free to use this project for learning and portfolio purposes.

## 👨‍💻 Author

Built as a comprehensive full-stack AI engineering project for interview preparation.

---

**Next Steps**: 
1. ✅ Complete MILESTONE 1
2. ⏳ MILESTONE 2 - UI Foundation (Landing page, design system)
3. ⏳ MILESTONE 3 - Firebase Authentication
