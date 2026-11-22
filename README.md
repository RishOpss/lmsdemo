# LMS Demo

A learning management system backend built with FastAPI, async SQLAlchemy and PostgreSQL (Supabase).

> **Status:** early development. Only a `/health` endpoint exists so far. The data models are defined, but the API routes, schemas and services are not implemented yet.

## Tech stack

- Python 3.12
- FastAPI + Uvicorn
- SQLAlchemy 2.x (async) with asyncpg
- Pydantic Settings for configuration
- Alembic (installed, migrations not set up yet)
- PostgreSQL hosted on Supabase

## Data model

`User`, `Course`, `Module`, `Lesson`, `Enrollment`, `LessonProgress`

## Project structure

```
backend/
├── app/
│   ├── main.py        # FastAPI app and lifespan
│   ├── core/config.py # Settings loaded from .env
│   ├── db/            # Declarative base and async engine/session
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas (to do)
│   ├── services/      # Business logic (to do)
│   └── api/           # Routers (to do)
└── requirements.txt
```

## Getting started

### 1. Install dependencies

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure the environment

Create `backend/.env`:

```
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:5432/postgres
SQL_ECHO=false
```

For Supabase, use the **Session pooler** connection string (the username is `postgres.<project-ref>`). The direct `db.<ref>.supabase.co` host is IPv6-only and fails on networks without IPv6, such as many WSL2 setups.

Never commit `.env`. It is listed in `.gitignore`.

### 3. Run the server

Run from the `backend/` directory so the `app` package can be imported:

```bash
uvicorn app.main:app --reload
```

- Health check: http://127.0.0.1:8000/health
- Interactive docs: http://127.0.0.1:8000/docs


## Docker

### Build the image

Run from the project root:

```bash
docker build -t lms-backend .
```

### Run the container

Provide your database configuration through environment variables:

```bash
docker run -d \
  --name lms-container \
  -p 8000:8000 \
  --env-file backend/.env \
  lms-backend
```

### Access the API

- Health: http://localhost:8000/health
- API documentation: http://localhost:8000/docs

### Stop the container

```bash
docker stop lms-container
docker rm lms-container
```

Note: The current application lifecycle drops registered
database tables during shutdown.


## Notes

- On startup, the app creates any missing tables with `Base.metadata.create_all`.
- Alembic is installed but not configured. Use it for schema changes once the models settle.
