import os

from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client,Client

from routers.auth import router as auth_router
from routers.protected import router as protected_router

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase:Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI(
    title= "Auth login and protected API",
    description= "FastAPI authentication API using Supabase Auth",
    version = "1.0.0"
)

app.include_router(auth_router)
app.include_router(protected_router)

@app.get("/")
def root():
    return {
        "message" : "Auth API is running.",
        "Status" : "Supabase Connected"
    }