"""FastAPI Web API template"""
from rich.console import Console
from .base import ProjectTemplate

console = Console()


class FastAPITemplate(ProjectTemplate):
    """Template for FastAPI Web API"""
    
    name = "FastAPI Web API"
    description = "REST API with FastAPI, database integration, and Docker support"
    
    def generate(self):
        console.print("[cyan]Creating FastAPI project...[/cyan]")
        
        # Create folders
        self.create_folder_structure(["src", "src/api", "src/models", "src/services", "src/db"])
        
        # Dependencies (without extra quotes)
        deps = [
            '"fastapi>=0.104.0"',
            '"uvicorn[standard]>=0.24.0"',
            '"sqlalchemy>=2.0.0"',
            '"alembic>=1.12.0"',
            '"pydantic>=2.4.0"',
            '"pydantic-settings>=2.0.0"',
            '"python-jose[cryptography]>=3.3.0"',
            '"passlib[bcrypt]>=1.7.4"',
            '"python-multipart>=0.0.6"',
        ]
        self.create_pyproject_toml(deps)
        
        # Create app structure
        self._create_main_app()
        self._create_dockerfile()
        self._create_docker_compose()
        self.create_src_init()
        
        # Create README
        readme = f'''# {self.project_name}

A FastAPI web application with database integration and authentication.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Run the development server:
```bash
uv run uvicorn src.main:app --reload
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment

Build and run with Docker:
```bash
docker-compose up --build
```

## Project Structure

- `src/api/` - API endpoints
- `src/models/` - Database models
- `src/services/` - Business logic
- `src/db/` - Database configuration
- `tests/` - Test suite

## Testing

```bash
uv run pytest
```
'''
        self.create_readme(readme)
        self.create_gitignore()
        self.create_basic_test()
        
        console.print("[green]✓ FastAPI project created successfully![/green]")
    
    def _create_main_app(self):
        content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API",
    description="A FastAPI application",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
'''
        with open(self.project_path / "src" / "main.py", "w") as f:
            f.write(content)
        
        (self.project_path / "src" / "api" / "__init__.py").touch()
        (self.project_path / "src" / "models" / "__init__.py").touch()
        (self.project_path / "src" / "services" / "__init__.py").touch()
        (self.project_path / "src" / "db" / "__init__.py").touch()
    
    def _create_dockerfile(self):
        content = '''FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml ./
COPY src ./src

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        with open(self.project_path / "Dockerfile", "w") as f:
            f.write(content)
    
    def _create_docker_compose(self):
        content = '''version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
    depends_on:
      - db
    volumes:
      - ./src:/app/src
    
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
'''
        with open(self.project_path / "docker-compose.yml", "w") as f:
            f.write(content)

