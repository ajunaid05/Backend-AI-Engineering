from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import sqlite3


conn = sqlite3.connect("tasks.db",check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    title TEXT,
    done BOOLEAN
    )
    """)
tasks = [
       {"id" : 1,"title":"Analyze the document","done":True},
       {"id" : 2,"title":"Make SRS","done":False},
       {"id" : 3,"title":"Implementation","done":False}
]

cursor.execute("SELECT COUNT(*) from tasks")
count = cursor.fetchone()[0]

if count == 0:
    for task in tasks:
        cursor.execute("""
           INSERT INTO tasks (id, title, done)
           VALUES (?,?,?)
           """,
           (task['id'],task['title'],task['done'])
)

conn.commit()

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
    title = task.title.strip()
    if not title:
#  Exceptions Handling Manually
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    cursor.execute("""
        INSERT INTO tasks (title,done)
        VALUES (?,?)
        """,
        (title,False)
        )
    conn.commit()
    new_task={
        "id" : cursor.lastrowid,
        "title" : title,
        "done" : False
    }
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
    cursor.execute("Select * from tasks")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        task = {
        "id" : row['id'],
        "title" : row['title'],
        "done" : bool(row['done'])
         }
        result.append(task)
    return result
conn.commit()

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
    cursor.execute("SELECT * FROM tasks WHERE id = ?",(id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
        status_code = 404,
        detail = f"Task with ID {id} not found."
    )
    task = {
        "id" : row['id'],
        "title" : row['title'],
        "done" : bool(row['done'])
             }
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

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="title cannot be empty."
        )
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
    cursor.execute("""
    UPDATE tasks
    SET title = ?, done = ?
    where id = ?
    """,
    (task.title.strip(),task.done,id)
    )

    conn.commit()

    # 5. Get updated task
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    # 6. Return API response
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

# Delete API(DELETE)

@app.delete("/tasks/{id}",
        status_code=204,
        summary="Delete a task",
        description="Deletes a task using its ID."
    )
def del_task(id: int):
    cursor.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (id,)
        )
    
    existing_task = cursor.fetchone()
    
    if existing_task is None:
            raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )
    cursor.execute("""
    DELETE FROM tasks WHERE id = ?
    """,(id,)
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


        