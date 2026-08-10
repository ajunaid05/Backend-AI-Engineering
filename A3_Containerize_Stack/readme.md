# Backend AI Engineering — Assignment 3

## Overview

A containerized Task Management CRUD API built with FastAPI and PostgreSQL. This project extends the previous SQLite-based CRUD API by replacing SQLite with PostgreSQL and containerizing the application and database using Docker Compose.

The application provides RESTful CRUD endpoints, request validation, exception handling, Swagger documentation, persistent PostgreSQL storage, and a reproducible Docker-based development environment.

## Features

- Create a new task
- Retrieve all tasks
- Retrieve a task by ID
- Update an existing task
- Delete a task
- Request validation using Pydantic
- Custom validation error handling
- HTTP exception handling
- Interactive API documentation with Swagger UI
- PostgreSQL database integration
- Dockerized FastAPI application
- Dockerized PostgreSQL database
- Docker Compose orchestration
- PostgreSQL health check
- Persistent database storage using a Docker named volume
- Database schema initialization through schema.sql
- Environment-based database configuration
- Data survives container restarts and docker compose down/up cycles

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- PostgreSQL 17
- psycopg2-binary
- python-dotenv
- Docker
- Docker Compose

## Project Structure

```
A3_Containerize_Stack/
├── main.py
├── repository.py
├── schema.sql
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── readme.md
└── Images/
```

## PostgreSQL Database

This version uses PostgreSQL instead of SQLite.

PostgreSQL runs inside a Docker container named a3-postgres. The database is named tasks.

Schema:

```
tasks
├── id INTEGER PRIMARY KEY
├── title TEXT NOT NULL
└── done BOOLEAN NOT NULL DEFAULT FALSE
```

Database data is stored in the Docker named volume a3_postgres_data. Therefore, removing and recreating containers does not remove the database data as long as the volume is retained.

## Environment Variables

The application uses environment variables for PostgreSQL configuration.

Example:

```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=tasks
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Inside Docker Compose, POSTGRES_HOST is db because db is the PostgreSQL service name on the Docker Compose network.

Actual credentials are stored in .env and excluded from Git using .gitignore. .env.example contains placeholder values and is safe to commit.

## Dockerfile

The FastAPI application is packaged into a lightweight Python 3.12 image.

The Dockerfile uses python:3.12-slim, sets /app as the working directory, installs requirements, copies the application source, exposes port 8000, and starts Uvicorn on 0.0.0.0:8000.

## Docker Compose

Docker Compose manages two services.

**app:**
- Builds the FastAPI application from the Dockerfile.
- Runs the API on port 8000.
- Receives PostgreSQL configuration through environment variables.
- Depends on the database health check.

**db:**
- Uses PostgreSQL 17.
- Runs on port 5432.
- Stores data in the a3_postgres_data named volume.
- Uses schema.sql as an initialization script.
- Includes a pg_isready health check.

The services communicate through the Docker Compose network. FastAPI connects to PostgreSQL using hostname db.

## Database Persistence

PostgreSQL data is persisted using:

```
a3_postgres_data:/var/lib/postgresql/data
```

Task records remain available after:

```
docker compose down
docker compose up
```

Data is removed only if the volume is explicitly deleted, for example:

```
docker compose down -v
```

## Installation

Clone the repository:

```
git clone https://github.com/ajunaid05/Backend-AI-Engineering.git
cd Backend-AI-Engineering
cd A3_Containerize_Stack
```

Make sure Docker Desktop is installed and running.

Create the .env file using .env.example and provide the required PostgreSQL configuration.

## Run the Application

Build and start:

```
docker compose up --build
```

Run detached:

```
docker compose up --build -d
```

Check containers:

```
docker compose ps
```

View application logs:

```
docker compose logs app
```

View PostgreSQL logs:

```
docker compose logs db
```

Stop:

```
docker compose down
```

## API Documentation

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Retrieve all tasks |
| GET | /tasks/{id} | Retrieve a task by ID |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update an existing task |
| DELETE | /tasks/{id} | Delete a task |

## Example API Request

Create a task through Swagger UI or curl:

```
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Learn Docker\",\"done\":false}"
```

Example response:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "done": false
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 OK | Request completed successfully |
| 201 Created | Resource created successfully |
| 204 No Content | Resource deleted successfully |
| 400 Bad Request | Invalid request or validation failed |
| 404 Not Found | Requested task was not found |

## Database Verification

Access PostgreSQL directly:

```
docker exec -it a3-postgres psql -U ahmad -d tasks
```

Useful commands:

```
\dt
\d tasks
SELECT * FROM tasks;
```

These commands were used to verify the tasks table and stored records.

## Testing Performed

- PostgreSQL container starts successfully.
- PostgreSQL reports a healthy status.
- FastAPI container starts successfully.
- FastAPI connects to PostgreSQL.
- GET /tasks retrieves database records.
- POST /tasks creates a task.
- GET /tasks/{id} retrieves a task.
- PUT /tasks/{id} updates a task.
- DELETE /tasks/{id} deletes a task.
- Missing task IDs return 404.
- Invalid request data is rejected.
- docker compose down followed by docker compose up preserves task data.
- docker compose config successfully validates the Compose configuration.

## Learning Outcomes

- RESTful API development with FastAPI
- CRUD operations
- Pydantic validation
- HTTP exception handling
- PostgreSQL integration with psycopg2
- Parameterized SQL queries
- Repository-layer database operations
- Docker image creation
- Docker containers
- Docker networking
- Docker Compose
- Container health checks
- Named Docker volumes
- Persistent database storage
- Environment variables
- Multi-container architecture
- Swagger UI testing
- PostgreSQL inspection using psql

## Architecture

```
Client / Swagger UI
        |
        v
FastAPI Container
  (a3-fastapi)
        |
        | Docker Compose Network
        v
PostgreSQL Container
  (a3-postgres)
        |
        v
Named Docker Volume
  (a3_postgres_data)
```

FastAPI handles HTTP requests and delegates database operations to repository.py. PostgreSQL provides persistent task storage.


**What I implemented and verified:**
- Created the project structure.
- Created and configured PostgreSQL.
- Created schema.sql.
- Implemented repository.py using psycopg2.
- Migrated CRUD operations from SQLite to PostgreSQL.
- Implemented FastAPI endpoints.
- Created Dockerfile and docker-compose.yml.
- Configured PostgreSQL health checks.
- Configured persistent Docker storage.
- Tested the API through Swagger UI.
- Verified database persistence across docker compose down/up.

## Author

**Ahmad Junaid**

Backend AI Engineering — Assignment 3
COMSATS University Lahore