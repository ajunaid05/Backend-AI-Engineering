from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app=FastAPI()
tasks = [{"id" : 1,"title":"Analyze the document","done":True},
       {"id" : 2,"title":"Make SRS","done":False},
       {"id" : 3,"title":"Implementation","done":False}]

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

@app.post("/tasks",status_code=201)
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


@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
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

@app.put("/tasks/{id}")
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

@app.delete("/tasks/{id}",status_code=204)
def del_task(id: int):
    for existing_task in tasks:
        if existing_task['id'] == id:
            tasks.remove(existing_task)
            return None
    raise HTTPException(
        status_code=404,
        detail="Given ID not found."
    )