from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import repository



app=FastAPI(title="Task API",
    description="A simple CRUD API built with FastAPI.",
    version="1.0.0")


# Create API(Post)

class TaskCreate(BaseModel):
    title : str
    done :  bool

# FastAPI exception Handling
@app.exception_handler(RequestValidationError)
async def exception_validator(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "Details": "Invalid Request",
            "Error": exc.errors()
        }
    )
# Create New Task
@app.post("/tasks",
          status_code=201,
          summary="Create a new task",
          description="Creates a new task with a unique ID and marks it as not completed.")
def create_task(task:TaskCreate):
    return repository.create_task(task.title,task.done)


#Get all tasks
@app.get("/tasks",
         summary="Get All Tasks",
         description="Get all tasks, Done and Pending Tasks."
         )
def get_tasks():
    return repository.get_alltasks()


#Get (By ID)
@app.get("/tasks/{id}",
         summary="Get a task",
         description="Returns a single task by its ID.")
def get_task_id(id: int):
    task = repository.get_task(id)
    if task is None:
        raise HTTPException(
        status_code = 404,
        detail = f"Task with ID {id} not found.")
    return task
    

# Update API(Put)

class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.put("/tasks/{id}",
         summary="Update a task",
         description="Updates the title and completion status of an existing task."
         )
def update_task(id: int,task: TaskUpdate):
    return repository.update_tasks(id,task.title,task.done)

# Delete API(DELETE)

@app.delete("/tasks/{id}",
        status_code=204,
        summary="Delete a task",
        description="Deletes a task using its ID."
    )
def del_task(id: int):
    deleted = repository.del_task(id)
    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {id} not found."
        )

    return deleted