from fastapi import FastAPI

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