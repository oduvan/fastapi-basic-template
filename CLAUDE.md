# FastAPI Basic Template - Project Reference

## Project Specification
**Source:** `claude_requests/project_definition.md` - Full requirements and tech stack

## Project Structure

```
app/
├── core/           # Config (config.py), database (database.py), exceptions
├── common/         # Shared utilities: pagination.py, filtering.py, sorting.py
├── models/         # Base SQLAlchemy model with timestamps
└── {domain}/       # Feature modules (items, files, tasks, websocket, pages)
    ├── router.py       # FastAPI endpoints
    ├── service.py      # Business logic
    ├── models.py       # SQLAlchemy models
    ├── schemas.py      # Pydantic validation
    ├── dependencies.py # FastAPI dependencies
    ├── exceptions.py   # Custom exceptions
    └── constants.py    # Domain constants

tests/              # pytest tests (100% coverage)
├── conftest.py         # Shared fixtures (client, db_session)
├── factories.py        # factory_boy test data factories
└── test_*.py           # Test files

alembic/            # Database migrations
├── versions/           # Migration files
└── env.py             # Alembic config (async setup)

docker/             # Dockerfiles and requirements
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
└── postcss/        # PostCSS container config

static/             # Static files (compiled CSS)
templates/          # Jinja2 templates
assets/             # Source files (CSS before PostCSS)
uploads/            # User uploaded files
```

## Key Files

- **app/main.py** - FastAPI application entry point, router registration
- **app/core/config.py** - Pydantic Settings (all env vars)
- **app/core/database.py** - Async SQLAlchemy setup
- **app/models/base.py** - Base model with id, created_at, updated_at
- **cli.py** - Typer CLI commands (seed-db, list-items, etc.)
- **docker-compose.yml** - Services: app, postgres, redis, postcss
- **Makefile** - All development commands
- **pyproject.toml** - Pytest, Ruff, coverage config
- **.pre-commit-config.yaml** - Pre-commit hooks (Python 3.14 venv)
- **.env** / **.env.example** - Environment variables

## Makefile Commands (Primary Tool)

**Services:**
- `make up` - Start all Docker services
- `make down` - Stop services
- `make restart` - Restart services
- `make logs` - View logs
- `make shell` - Open shell in app container

**Database:**
- `make migrate` - Apply migrations
- `make makemigrations` - Create new migration (prompts for message)

**Testing:**
- `make test` - Run pytest
- `make coverage` - Run tests with coverage report (opens htmlcov/)

**Code Quality:**
- `make format` - Format with Ruff
- `make lint` - Lint with Ruff
- `make pre-commit-install` - Setup pre-commit hooks

**Maintenance:**
- `make update-python` - Update Python dependencies
- `make update-frontend` - Update Node/PostCSS dependencies
- `make clean` - Clean containers, volumes, cache

**Help:**
- `make help` - Show all commands

## CLI Commands (inside container)

```bash
docker compose exec app python cli.py <command>

# Available commands:
info          # App information
create-db     # Create tables
drop-db       # Drop all tables
seed-db       # Seed sample data
list-items    # List all items
count-items   # Count items
clear-items   # Delete all items
shell         # Python REPL
```

## Tech Stack

**Core:** FastAPI + Uvicorn + SQLAlchemy 2.0 (async) + Alembic
**Database:** PostgreSQL 16 + asyncpg
**Cache/Rate Limit:** Redis 7 + fastapi-cache2 + slowapi
**Validation:** Pydantic v2
**Templates:** Jinja2 + PostCSS
**Testing:** pytest + pytest-asyncio + httpx + factory-boy + pytest-cov + pytest-mock + freezegun
**Code Quality:** Ruff + pre-commit
**CLI:** Typer + Rich

## Architecture Patterns

**Layered structure:** Router → Service → Model
**All async:** Use async/await for DB, file operations
**Dependency injection:** FastAPI's Depends() system
**Type hints:** Full typing everywhere
**Base model:** All models inherit id, created_at, updated_at from BaseModel

## Docker Services

- **app** (port 8000) - FastAPI with hot reload
- **postgres** (port 5432) - PostgreSQL 16
- **redis** (port 6379) - Redis 7
- **postcss** - Watches `assets/css/` → compiles to `static/css/`

## Configuration

All settings in `.env` file (see `.env.example`)
Loaded via `app/core/config.py` (Pydantic Settings)
Auto-constructed: DATABASE_URL, REDIS_URL

## Testing

- **Test DB:** PostgreSQL (uses same container, separate database: `fastapi_db_test`)
- **Key fixtures:** `client` (AsyncClient), `db_session` (clean DB per test)
- **Location:** `tests/conftest.py`
- **Coverage target:** 100%

## Pre-commit

- **Venv:** Separate Python 3.14 venv (`.venv-precommit/`)
- **Install:** `make pre-commit-install`
- **Hooks:** Ruff (lint + format), YAML/JSON validation, trailing whitespace, etc.

## API Documentation

- **Swagger:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Development Workflow

1. Use **Makefile** for all common tasks
2. Models → Services → Routers → Tests
3. Register new routers in `app/main.py`
4. Import ALL models in `app/models/__init__.py` for Alembic detection
5. Run `make makemigrations` → `make migrate` after model changes
6. Always write tests (use factories for test data)
7. Use `make format` before committing

## ⚠️ CRITICAL: Testing Protocol

**ALWAYS run tests after making structural changes:**

**Command:** `make test`
