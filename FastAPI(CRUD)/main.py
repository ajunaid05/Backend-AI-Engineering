from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

tasks = [
       {"id" : 1,"title":"Analyze the document","done":True},
       {"id" : 2,"title":"Make SRS","done":False},
       {"id" : 3,"title":"Implementation","done":False}
]


og_tasks=[
       {"id" : 1,"title":"Analyze the document","done":True},
       {"id" : 2,"title":"Make SRS","done":False},
       {"id" : 3,"title":"Implementation","done":False}
]


app=FastAPI(title="Task API",
    description="A simple CRUD API built with FastAPI.",
    version="1.0.0")


# Create API(Post)

class TaskCreate(BaseModel):
    title : str

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

@app.post("/tasks",
          status_code=201,
          summary="Create a new task",
          description="Creates a new task with a unique ID and marks it as not completed.")
def create_task(task:TaskCreate):
    if task.title.strip()=="":
#  Exceptions Handling Manually
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    new_task={
        "id" : len(tasks)+1,
        "title" : task.title,
        "done" : False
    }
    tasks.append(new_task)
    return new_task

# Print API(Get)

@app.get("/")
def root():
    return {
        "Name" : "Task API",
        "Version" : "1.0",
        "Endpoints" : ["/tasks"]
    }

@app.get("/health")
def health():
    return {
        "Status" : "OK"
    }

#Get tasks filter and without filter
@app.get("/tasks",
         summary="Search Tasks",
         description="Get all tasks, Done and Pending Tasks and search tasks with any perameter"
         )
def search_tasks(search: Optional[str] = None,done: Optional[bool] = None):
    filtered_tasks=[]
    if done is None and search is None:
        return tasks
    for task in tasks:
        if done is not None and task["done"]!=done:
            continue
        if search is not None and search.lower() not in task['title'].lower():
            continue
        filtered_tasks.append(task)
    return filtered_tasks

@app.get("/reset",
         summary="Reset Tasks",
         description="Instead of restarting server reset garbadge data with orignal.")
def reset_tasks():
    global tasks
    tasks=[task.copy() for task in og_tasks]
    return tasks

#Get (By ID)
@app.get("/tasks/{id}",
         summary="Get a task",
         description="Returns a single task by its ID.")
def get_task_id(id: int):
    for task in tasks:
        if task['id'] == id:
            return task

    raise HTTPException(
        status_code = 404,
        detail = f"Task with ID {id} not found."
    )

# Update API(Put)

class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.put("/tasks/{id}",
         summary="Update a task",
         description="Updates the title and completion status of an existing task."
         )
def update_task(id: int,task: TaskUpdate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="title cannot be empty."
        )
    for existing_task in tasks:
        if existing_task['id']==id:
            existing_task['title'] = task.title
            existing_task['done'] = task.done

            return existing_task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# Delete API(DELETE)

@app.delete("/tasks/{id}",
        status_code=204,
        summary="Delete a task",
        description="Deletes a task using its ID."
    )
def del_task(id: int):
    for existing_task in tasks:
        if existing_task['id'] == id:
            tasks.remove(existing_task)
            return None
    raise HTTPException(
        status_code=404,
        detail="Given ID not found."
    )

 #Get Stats

@app.get("/stats", summary="Get Tasks Statistics", description="Get Description of total tasks, pending ones and competed tasks")
def task_stats():
    competed=0
    pending=0
    for task in tasks:
        if task['done']==True:
            competed=competed+1
        else:
            pending=pending+1
    return {
        "Total" : len(tasks),
        "done" : competed,
        "pending" : pending
    }


        