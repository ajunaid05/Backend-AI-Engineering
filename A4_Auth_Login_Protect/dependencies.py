from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database import supabase

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

    except Exception as e:
        print("Supabase verification Error.",e)

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )
    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )
    return response.user

def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    return token

    
    
