from fastapi import FastAPI, HTTPException

app=FastAPI()

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

tasks = [{"id" : 1,"title":"Analyze the document","done":True},
       {"id" : 2,"title":"Make SRS","done":False},
       {"id" : 3,"title":"Implementation","done":False}]
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