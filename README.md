# FastAPI Basic Template

A comprehensive FastAPI project template with production-ready features and best practices.

## Features

### Core Functionality
- ✅ **CRUD Operations** - Full Create, Read, Update, Delete with async SQLAlchemy
- ✅ **Pagination** - Flexible pagination with customizable page sizes
- ✅ **Filtering & Sorting** - Advanced query capabilities
- ✅ **File Upload/Download** - Secure file handling with size limits
- ✅ **WebSocket Support** - Real-time communication example
- ✅ **Background Tasks** - Async task processing with FastAPI BackgroundTasks
- ✅ **Caching** - Redis caching with fastapi-cache2
- ✅ **Rate Limiting** - Protection against abuse with slowapi
- ✅ **Admin Panel** - SQLAdmin with authentication
- ✅ **Templates** - Jinja2 templates with PostCSS styling

### Tech Stack
- **Python 3.14** - Latest stable Python
- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Production database with asyncpg
- **Redis** - Caching and session storage
- **SQLAlchemy 2.0** - Async ORM
- **Alembic** - Database migrations
- **Pydantic v2** - Data validation
- **Docker Compose** - Easy development setup

### Development Tools
- **Ruff** - Fast Python linter and formatter
- **pytest** - Comprehensive test suite
- **pytest-cov** - Code coverage reporting
- **factory_boy** - Test data factories
- **pre-commit** - Git hooks for code quality
- **Typer & Rich** - Beautiful CLI commands
- **PostCSS** - CSS processing with autoprefixer and nesting

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-basic-template
   ```

2. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start services**
   ```bash
   make up
   ```

4. **Install frontend dependencies and build CSS**
   ```bash
   docker-compose exec postcss npm install
   ```

5. **Run migrations**
   ```bash
   make migrate
   ```

6. **Access the application**
   - API: http://localhost:8000
   - API Docs (Swagger): http://localhost:8000/docs
   - API Docs (ReDoc): http://localhost:8000/redoc
   - Admin Panel: http://localhost:8000/admin (default: admin/admin)
   - WebSocket Test: http://localhost:8000/ws/test

## Makefile Commands

All common operations are available through make commands:

```bash
make help                 # Show all available commands
make build                # Build Docker images
make up                   # Start all services
make down                 # Stop all services
make restart              # Restart all services
make logs                 # View logs
make shell                # Open shell in app container
make test                 # Run tests
make coverage             # Run tests with coverage report
make format               # Format code with ruff
make lint                 # Lint code with ruff
make migrate              # Run database migrations
make makemigrations       # Create new migration
make update-python        # Update Python dependencies
make update-frontend      # Update frontend dependencies
make pre-commit-install   # Install pre-commit hooks
make clean                # Clean up containers and volumes
```

## CLI Commands

The project includes a powerful CLI built with Typer and Rich:

```bash
# Inside the container
docker-compose exec app python cli.py --help

# Available commands:
python cli.py info              # Display application information
python cli.py create-db         # Create database tables
python cli.py drop-db           # Drop all database tables
python cli.py seed-db           # Seed database with sample data
python cli.py list-items        # List items from database
python cli.py count-items       # Count total items
python cli.py clear-items       # Delete all items
python cli.py shell             # Interactive Python shell
```

## Project Structure

```
fastapi-basic-template/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration files
│   └── env.py                 # Alembic configuration
├── app/                        # Application code
│   ├── api/                   # API routes
│   │   └── v1/
│   │       ├── endpoints/     # API endpoints
│   │       └── api.py         # Router configuration
│   ├── core/                  # Core functionality
│   │   ├── admin.py          # Admin authentication
│   │   └── admin_views.py    # Admin model views
│   ├── models/                # Database models
│   │   ├── base.py           # Base model with timestamps
│   │   └── item.py           # Example model
│   ├── schemas/               # Pydantic schemas
│   │   └── item.py           # Item schemas
│   ├── services/              # Business logic
│   │   └── item.py           # Item service
│   ├── utils/                 # Utilities
│   │   ├── filtering.py      # Filtering utilities
│   │   ├── pagination.py     # Pagination utilities
│   │   └── sorting.py        # Sorting utilities
│   ├── config.py              # Settings management
│   ├── database.py            # Database session
│   └── main.py                # FastAPI application
├── postcss/                   # PostCSS configuration
│   ├── src/                  # Source CSS files
│   ├── package.json          # Node dependencies
│   └── postcss.config.js     # PostCSS config
├── static/                    # Static files
│   └── css/                  # Compiled CSS
├── templates/                 # Jinja2 templates
│   └── index.html            # Example template
├── tests/                     # Test suite
│   ├── conftest.py           # Pytest fixtures
│   ├── factories.py          # Test data factories
│   ├── test_items.py         # Item tests
│   ├── test_files.py         # File upload tests
│   ├── test_tasks.py         # Background task tests
│   └── test_main.py          # Main app tests
├── uploads/                   # Uploaded files
├── .env                       # Environment variables
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
├── .pre-commit-config.yaml    # Pre-commit hooks
├── alembic.ini                # Alembic configuration
├── cli.py                     # CLI commands
├── docker-compose.yml         # Docker services
├── Dockerfile                 # App container
├── Makefile                   # Common commands
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Dev dependencies
└── requirements-precommit.txt # Pre-commit dependencies
```

## API Endpoints

### Items (CRUD)
- `GET /items/` - List items (with pagination, filtering, sorting)
- `GET /items/{id}` - Get item by ID (cached)
- `POST /items/` - Create item (rate limited)
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

### Files
- `POST /files/upload` - Upload file (rate limited)
- `GET /files/download/{filename}` - Download file
- `GET /files/list` - List uploaded files
- `DELETE /files/{filename}` - Delete file

### WebSocket
- `WS /ws/chat` - WebSocket chat endpoint
- `GET /ws/test` - WebSocket test page

### Background Tasks
- `POST /tasks/send-email` - Queue email task
- `POST /tasks/process-data` - Queue data processing task
- `POST /tasks/log` - Queue logging task
- `POST /tasks/multiple-tasks` - Queue multiple tasks

### Pages
- `GET /pages/` - Example Jinja2 template page

## Testing

The project includes comprehensive tests for all features:

```bash
# Run all tests
make test

# Run tests with coverage
make coverage

# Run specific test file
docker-compose exec app pytest tests/test_items.py

# Run tests with verbose output
docker-compose exec app pytest -v

# Run tests matching a pattern
docker-compose exec app pytest -k "test_create"
```

Test coverage includes:
- CRUD operations
- Pagination, filtering, sorting
- File upload/download
- Background tasks
- Caching
- Rate limiting
- WebSocket connections
- Main application endpoints

## Database Migrations

```bash
# Create a new migration
make makemigrations

# Apply migrations
make migrate

# View migration history
docker-compose exec app alembic history

# Downgrade one revision
docker-compose exec app alembic downgrade -1

# Upgrade to specific revision
docker-compose exec app alembic upgrade <revision>
```

## Code Quality

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
make pre-commit-install
```

This will run on every commit:
- Ruff linting and formatting
- Trailing whitespace removal
- YAML/JSON/TOML validation
- Large file detection
- Private key detection

### Manual Formatting and Linting

```bash
# Format code
make format

# Lint code
make lint
```

## Configuration

All configuration is managed through environment variables in `.env`:

### Application
- `APP_NAME` - Application name
- `APP_VERSION` - Application version
- `DEBUG` - Debug mode (True/False)
- `ENVIRONMENT` - Environment (development/production)

### API
- `SECRET_KEY` - Secret key for security

### Database
- `POSTGRES_SERVER` - PostgreSQL host
- `POSTGRES_PORT` - PostgreSQL port
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name
- `DATABASE_URL` - Full database URL

### Redis
- `REDIS_HOST` - Redis host
- `REDIS_PORT` - Redis port
- `REDIS_DB` - Redis database number
- `REDIS_URL` - Full Redis URL

### Security
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins
- `RATE_LIMIT_PER_MINUTE` - Rate limit threshold
- `ADMIN_SECRET_KEY` - Admin panel secret key
- `ADMIN_USERNAME` - Admin username
- `ADMIN_PASSWORD` - Admin password

### File Upload
- `MAX_UPLOAD_SIZE` - Maximum file size (bytes)
- `UPLOAD_DIR` - Upload directory path

## Production Deployment

For production deployment:

1. **Update environment variables**
   - Change `DEBUG` to `False`
   - Set strong `SECRET_KEY` and `ADMIN_SECRET_KEY`
   - Update `BACKEND_CORS_ORIGINS`
   - Use strong database and admin credentials

2. **Use production database**
   - Set up PostgreSQL instance
   - Update `DATABASE_URL`

3. **Use production Redis**
   - Set up Redis instance
   - Update `REDIS_URL`

4. **Configure SSL/TLS**
   - Use a reverse proxy (nginx, traefik)
   - Enable HTTPS

5. **Set up monitoring**
   - Application logging
   - Database monitoring
   - Performance metrics

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

7. **Use production server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## Best Practices

This template follows the best practices from:
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- FastAPI official documentation
- SQLAlchemy 2.0 best practices
- Python typing and async/await patterns

### Key Principles
- Async/await throughout
- Dependency injection
- Proper error handling
- Type hints everywhere
- Comprehensive testing
- Clean architecture
- Security by default

## License

MIT License - Feel free to use this template for your projects!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the repository.
