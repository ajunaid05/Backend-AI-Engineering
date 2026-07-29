from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ==========================================================
# FastAPI Application Configuration
# ==========================================================

app = FastAPI(
    title="Task Management API",
    description="A simple RESTful Task Management API using FastAPI and in-memory storage.",
    version="1.0.0",
)

# ==========================================================
# Sample Data
# ==========================================================

ORIGINAL_TASKS = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Make SRS", "done": False},
    {"id": 3, "title": "Submit Assignment", "done": True},
]

tasks = [task.copy() for task in ORIGINAL_TASKS]

# ==========================================================
# Pydantic Models
# ==========================================================

class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str = Field(..., description="Task title")


class TaskUpdate(BaseModel):
    title: str
    done: bool


class HealthResponse(BaseModel):
    status: str


class StatsResponse(BaseModel):
    total: int
    completed: int
    pending: int


# ==========================================================
# Custom Validation Error Handler
# Returns 400 instead of FastAPI's default 422
# ==========================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "message": "Validation Error",
            "errors": exc.errors(),
        },
    )


# ==========================================================
# Helper Functions
# ==========================================================

def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def next_task_id():
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# ==========================================================
# API Endpoints
# ==========================================================

@app.get(
    "/",
    summary="API Information",
    description="Returns basic information about the API.",
)
def root():
    return {
        "message": "Welcome to Task Management API",
        "version": "1.0.0",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns server health status.",
)
def health():
    return {"status": "healthy"}


@app.get(
    "/tasks",
    response_model=List[Task],
    summary="Get All Tasks",
    description="Returns all tasks. Supports filtering by completion status and searching by title.",
)
def get_tasks(
    done: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
):
    result = tasks

    if done is not None:
        result = [task for task in result if task["done"] == done]

    if search:
        result = [
            task
            for task in result
            if search.lower() in task["title"].lower()
        ]

    return result


@app.get(
    "/tasks/{id}",
    response_model=Task,
    summary="Get Task By ID",
    description="Returns a single task using its ID.",
)
def get_single_task(id: int):
    task = get_task(id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create Task",
    description="Creates a new task.",
)
def create_task(task: TaskCreate):
    title = task.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty",
        )

    new_task = {
        "id": next_task_id(),
        "title": title,
        "done": False,
    }

    tasks.append(new_task)

    return new_task


@app.put(
    "/tasks/{id}",
    response_model=Task,
    summary="Update Task",
    description="Updates the title and completion status of a task.",
)
def update_task(id: int, updated: TaskUpdate):
    task = get_task(id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    title = updated.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty",
        )

    task["title"] = title
    task["done"] = updated.done

    return task


@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Task",
    description="Deletes a task by ID.",
)
def delete_task(id: int):
    task = get_task(id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    tasks.remove(task)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get(
    "/stats",
    response_model=StatsResponse,
    summary="Task Statistics",
    description="Returns total, completed and pending task counts.",
)
def stats():
    completed = sum(task["done"] for task in tasks)

    return {
        "total": len(tasks),
        "completed": completed,
        "pending": len(tasks) - completed,
    }


@app.post(
    "/reset",
    summary="Reset Tasks",
    description="Restores the original sample tasks.",
)
def reset():
    tasks.clear()
    tasks.extend(task.copy() for task in ORIGINAL_TASKS)

    return {
        "message": "Tasks reset successfully",
        "tasks": tasks,
    }