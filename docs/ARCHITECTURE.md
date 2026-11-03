# SchemaGenius AI - System Architecture

This document describes the technical architecture and design decisions for SchemaGenius AI.

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Security Architecture](#security-architecture)
- [Database Design](#database-design)
- [API Design](#api-design)
- [Deployment Architecture](#deployment-architecture)

---

## Overview

SchemaGenius AI is a full-stack AI-powered platform for converting natural language requirements into production-ready database schemas. The system uses a decoupled frontend-backend architecture with external services for authentication, AI generation, and data persistence.

### Core Principles

1. **Security First**: Every request authenticated, user data isolated, secrets protected
2. **Deterministic Validation**: Schema validation uses rules, not AI guessing
3. **Canonical Model**: Internal JSON schema is the single source of truth
4. **Sandbox Isolation**: SQL testing completely separated from application data
5. **Extensibility**: Modular design supports future dialects and features

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │   React Frontend (TypeScript + Vite)                   │    │
│  │   Port: 5173 (dev) / Vercel (production)               │    │
│  │                                                         │    │
│  │   Components:                                           │    │
│  │   - Landing page, authentication UI                    │    │
│  │   - Dashboard, workspace                               │    │
│  │   - React Flow ER diagrams                             │    │
│  │   - Tailwind CSS + shadcn/ui                           │    │
│  │   - Firebase Auth SDK (client-side)                    │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↕ HTTPS (axios)
┌─────────────────────────────────────────────────────────────────┐
│              FIREBASE AUTHENTICATION                             │
│   - User registration, login, password reset                    │
│   - ID token generation and validation                          │
│   - Email verification                                          │
└─────────────────────────────────────────────────────────────────┘
                              ↕ Firebase Admin SDK
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND (Python)                     │
│   Port: 8000 (dev) / Render.com (production)                   │
│                                                                 │
│   ┌───────────────────────────────────────────────────────┐   │
│   │ API Layer (FastAPI)                                   │   │
│   │ - REST endpoints with OpenAPI documentation           │   │
│   │ - Request validation (Pydantic)                       │   │
│   │ - CORS middleware                                     │   │
│   │ - Firebase token verification                         │   │
│   │ - Rate limiting                                       │   │
│   └───────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌───────────────────────────────────────────────────────┐   │
│   │ Business Logic Layer                                  │   │
│   │ - Schema validation engine (deterministic rules)      │   │
│   │ - SQL generation (MySQL, PostgreSQL)                  │   │
│   │ - Normalization analyzer                              │   │
│   │ - Optimization suggester                              │   │
│   │ - Version management                                  │   │
│   └───────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌───────────────────────────────────────────────────────┐   │
│   │ AI Service Layer                                      │   │
│   │ - Gemini API integration                              │   │
│   │ - Structured output parsing                           │   │
│   │ - Retry logic with exponential backoff                │   │
│   │ - Response validation                                 │   │
│   └───────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌───────────────────────────────────────────────────────┐   │
│   │ Data Access Layer (SQLAlchemy)                        │   │
│   │ - ORM models                                          │   │
│   │ - Repository pattern                                  │   │
│   │ - Transaction management                              │   │
│   │ - Alembic migrations                                  │   │
│   └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
            ↕                        ↕                    ↕
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   PostgreSQL     │   │   PostgreSQL     │   │   Google Gemini  │
│   Application    │   │   SQL Sandbox    │   │   API            │
│   Database       │   │   (Isolated)     │   │                  │
│                  │   │                  │   │   - Schema Gen   │
│   Port: 5432     │   │   Port: 5433     │   │   - Structured   │
│   Docker         │   │   Docker         │   │     Output       │
└──────────────────┘   └──────────────────┘   └──────────────────┘
```

---

## Technology Stack

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2+ | UI framework |
| TypeScript | 5.3+ | Type safety |
| Vite | 5.0+ | Build tool and dev server |
| Tailwind CSS | 3.4+ | Utility-first styling |
| shadcn/ui | Latest | Component library |
| React Flow | @xyflow/react 12+ | Interactive ER diagrams |
| React Router | 6.21+ | Client-side routing |
| TanStack Query | 5.17+ | Server state management |
| React Hook Form | 7.49+ | Form handling |
| Zod | 3.22+ | Schema validation |
| Firebase SDK | 10.7+ | Authentication (client) |
| Axios | 1.6+ | HTTP client |
| Lucide React | Latest | Icon library |

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Programming language |
| FastAPI | 0.109+ | Web framework |
| Pydantic | 2.5+ | Data validation |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.13+ | Database migrations |
| PostgreSQL | 15+ | Database |
| psycopg2 | 2.9+ | PostgreSQL driver |
| Firebase Admin | 6.4+ | Authentication (server) |
| google-generativeai | Latest | Gemini AI SDK |
| Uvicorn | Latest | ASGI server |
| Pytest | Latest | Testing framework |

### Infrastructure

| Service | Purpose |
|---------|---------|
| Docker | Local PostgreSQL development |
| Vercel | Frontend hosting |
| Render.com | Backend hosting |
| Firebase | Authentication service |
| Google AI Studio | Gemini API |

---

## Data Flow

### 1. User Authentication Flow

```
User → Frontend (Firebase Auth SDK)
  ↓ Email/Password
Firebase Authentication Service
  ↓ ID Token
Frontend stores token
  ↓ Include in Authorization header
Backend → Firebase Admin SDK verification
  ↓ Extract user ID
Backend authorizes request
```

### 2. Schema Generation Flow

```
User enters requirements (natural language)
  ↓
Frontend validates input
  ↓ POST /api/v1/generation/generate
Backend authenticates user
  ↓
Backend calls Gemini API with structured prompt
  ↓ Returns JSON
Backend validates response with Pydantic
  ↓
Backend runs deterministic schema validation
  ↓
Backend saves to PostgreSQL (application DB)
  ↓ Returns validated schema
Frontend renders ER diagram with React Flow
```

### 3. SQL Generation Flow

```
User selects dialect (MySQL/PostgreSQL)
  ↓ GET /api/v1/sql/generate/{project_id}
Backend retrieves canonical schema from DB
  ↓
Backend runs deterministic SQL generator
  ↓ Applies dialect-specific rules
Backend returns formatted SQL
  ↓
Frontend displays with syntax highlighting
User can copy, download, or test in sandbox
```

### 4. SQL Sandbox Execution Flow

```
User submits SQL for testing
  ↓ POST /api/v1/sandbox/execute
Backend authenticates user
  ↓
Backend creates temporary database in sandbox PostgreSQL
  ↓ Executes SQL with strict timeouts and limits
Sandbox returns results
  ↓ Cleans up temporary database
Backend returns execution results to frontend
```

**Critical**: Sandbox PostgreSQL has NO access to:
- Application database
- Other users' data
- Host filesystem
- Internal services
- Environment variables with secrets

---

## Security Architecture

### Authentication & Authorization

1. **Frontend Authentication**
   - Firebase SDK handles user login/registration
   - ID token stored securely in memory (not localStorage)
   - Token included in every API request via `Authorization: Bearer <token>`

2. **Backend Verification**
   - Every protected endpoint verifies Firebase ID token
   - Token validation using Firebase Admin SDK
   - User ID extracted from verified token (never trusted from client)
   - User ownership checked for all resource operations

3. **Authorization Rules**
   - Users can only access their own projects
   - Schema modifications require project ownership
   - SQL sandbox sessions are user-isolated

### Data Protection

- **Secrets Management**
  - `.env` files never committed to Git
  - Service account keys stored outside repository
  - Environment variables for all sensitive config
  - Production secrets configured via hosting platform

- **CORS Configuration**
  - Whitelist only frontend origins
  - Credentials allowed for authenticated requests
  - No wildcard (*) origins in production

- **SQL Injection Prevention**
  - No raw SQL string concatenation
  - Parameterized queries for user data
  - SQL generation uses AST-based construction
  - Sandbox uses restricted database user

### Rate Limiting

| Endpoint Type | Limit |
|---------------|-------|
| AI Generation | 10 requests/minute |
| SQL Sandbox | 30 requests/minute |
| General API | 100 requests/minute |

---

## Database Design

### Application PostgreSQL Schema

```sql
-- Users table (synced with Firebase)
CREATE TABLE users (
    id UUID PRIMARY KEY,
    firebase_uid VARCHAR(128) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sql_dialect VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_user_projects (user_id, updated_at DESC)
);

-- Schema versions table
CREATE TABLE schema_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    schema_data JSONB NOT NULL,  -- Canonical schema model
    created_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    UNIQUE(project_id, version_number),
    INDEX idx_project_versions (project_id, version_number DESC)
);

-- Generation history (optional, for analytics)
CREATE TABLE generation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    requirements_text TEXT NOT NULL,
    gemini_model VARCHAR(100),
    success BOOLEAN NOT NULL,
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Canonical Schema Model (JSON)

Stored in `schema_versions.schema_data`:

```json
{
  "schemaId": "uuid",
  "schemaName": "string",
  "sqlDialect": "postgresql|mysql",
  "version": 1,
  "tables": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string",
      "columns": [
        {
          "id": "uuid",
          "name": "string",
          "dataType": "string",
          "nullable": boolean,
          "primaryKey": boolean,
          "unique": boolean,
          "defaultValue": "string|null",
          "description": "string"
        }
      ],
      "primaryKey": ["column_id"],
      "uniqueConstraints": [["column_id"]],
      "indexes": [
        {
          "name": "string",
          "columns": ["column_id"],
          "unique": boolean
        }
      ]
    }
  ],
  "relationships": [
    {
      "id": "uuid",
      "sourceTableId": "uuid",
      "sourceColumnId": "uuid",
      "targetTableId": "uuid",
      "targetColumnId": "uuid",
      "cardinality": "one-to-one|one-to-many|many-to-many",
      "onDelete": "CASCADE|SET NULL|RESTRICT|NO ACTION",
      "onUpdate": "CASCADE|SET NULL|RESTRICT|NO ACTION"
    }
  ],
  "metadata": {
    "generatedAt": "timestamp",
    "generatedBy": "user_id",
    "assumptions": ["string"]
  }
}
```

---

## API Design

### REST API Endpoints

Base URL: `http://localhost:8000` (dev) or `https://api.your-domain.com` (prod)

#### System Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/docs` - Swagger UI
- `GET /api/redoc` - ReDoc documentation

#### Authentication (Firebase-based)
- `GET /api/v1/auth/me` - Get current user profile
- `POST /api/v1/auth/sync` - Sync Firebase user to database

#### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List user's projects
- `GET /api/v1/projects/{id}` - Get project details
- `PATCH /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

#### Schema Generation
- `POST /api/v1/generation/generate` - Generate schema from requirements
- `POST /api/v1/generation/regenerate/{project_id}` - Regenerate with new requirements

#### Schema Management
- `GET /api/v1/schemas/{project_id}` - Get current schema
- `PUT /api/v1/schemas/{project_id}` - Update schema
- `GET /api/v1/schemas/{project_id}/versions` - List versions
- `POST /api/v1/schemas/{project_id}/versions` - Create new version
- `GET /api/v1/schemas/{project_id}/versions/{version}` - Get specific version

#### Validation
- `POST /api/v1/validation/validate` - Validate schema
- `GET /api/v1/validation/findings/{project_id}` - Get validation findings

#### SQL Generation
- `GET /api/v1/sql/generate/{project_id}` - Generate SQL for project
- `POST /api/v1/sql/export` - Export SQL file

#### SQL Sandbox
- `POST /api/v1/sandbox/execute` - Execute SQL in sandbox
- `GET /api/v1/sandbox/status/{session_id}` - Get execution status

#### Analysis
- `POST /api/v1/analysis/normalize` - Get normalization suggestions
- `POST /api/v1/analysis/optimize` - Get optimization recommendations

---

## Deployment Architecture

### Local Development

```
Frontend: http://localhost:5173 (Vite dev server)
Backend: http://localhost:8000 (Uvicorn)
PostgreSQL App: localhost:5432 (Docker)
PostgreSQL Sandbox: localhost:5433 (Docker)
```

### Production

```
Frontend: https://your-app.vercel.app (Vercel CDN)
  ↓ HTTPS
Backend: https://your-backend.onrender.com (Render.com)
  ↓
Application DB: Render.com PostgreSQL (managed)
Sandbox DB: Separate Render.com PostgreSQL (managed, isolated)
Firebase: Firebase Authentication (Google Cloud)
Gemini: Google AI Studio API (Google Cloud)
```

### Environment Variables

**Frontend (.env):**
```
VITE_API_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=<public-key>
VITE_FIREBASE_AUTH_DOMAIN=<domain>
VITE_FIREBASE_PROJECT_ID=<id>
...
```

**Backend (.env):**
```
DATABASE_URL=postgresql://user:pass@host:5432/db
SANDBOX_DATABASE_URL=postgresql://sandbox:pass@host:5433/sandbox
GEMINI_API_KEY=<secret-key>
FIREBASE_CREDENTIALS_PATH=/path/to/service-account.json
SECRET_KEY=<secret>
ALLOWED_ORIGINS=https://your-app.vercel.app
```

---

## Design Patterns

### Backend Patterns

1. **Repository Pattern**: Data access logic separated into repositories
2. **Service Layer**: Business logic isolated from API routes
3. **Dependency Injection**: FastAPI's Depends() for shared dependencies
4. **Factory Pattern**: Schema generator factory for different dialects
5. **Strategy Pattern**: SQL generation strategies per dialect

### Frontend Patterns

1. **Component Composition**: Small, reusable UI components
2. **Custom Hooks**: Shared logic in React hooks
3. **Context API**: Authentication state management
4. **TanStack Query**: Server state caching and synchronization
5. **Controlled Components**: Forms managed via React Hook Form

---

## Scalability Considerations

### Current Architecture (MVP)
- Suitable for 100s of concurrent users
- Synchronous AI generation (acceptable for <30s responses)
- Direct database connections

### Future Scaling Options
- **Async Generation**: Queue-based AI generation with background workers
- **Caching**: Redis for session and schema caching
- **Database Pooling**: PgBouncer for connection management
- **CDN**: Asset optimization and edge caching
- **Load Balancing**: Multiple backend instances
- **Microservices**: Separate sandbox service

---

## Testing Strategy

- **Unit Tests**: Schema validation, SQL generation, business logic
- **Integration Tests**: API endpoints, database operations
- **E2E Tests**: Complete user workflows
- **Security Tests**: Authentication, authorization, SQL injection
- **Performance Tests**: AI generation latency, database query performance

---

**Document Version**: 1.0  
**Last Updated**: 2026-11-03  
**Author**: SchemaGenius AI Development Team
