from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
from database import supabase
from dependencies import get_current_token
router = APIRouter(prefix = "/auth", tags = ["Authentication"])

class AuthRequest(BaseModel):
    email : str
    password : str


@router.post("/signup", status_code=201)
def sign_up(credentials: AuthRequest):
    if not credentials.email or not credentials.password:
        raise HTTPException(
            status_code=400,
            detail="Email and Password required."
        )

    response = supabase.auth.sign_up({
        "email" : credentials.email,
        "password" : credentials.password
    })

    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Unable to create user."
        )
    return {
        "message" : "User created successfully.",
        "user" : response.user
    }

@router.post('/login')
def login_user(credentials: AuthRequest):
    if not credentials.email or not credentials.password:
        raise HTTPException(
            status_code=400,
            detail="Email and Password required."
        )

    try:
        response = supabase.auth.sign_in_with_password({
                "email" : credentials.email,
                "password" : credentials.password
            })
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials."
        )

    if response.session is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid login credentials."
        )
    return {
        "access_token" : response.session.access_token,
        "refresh_token" : response.session.refresh_token
    }

@router.post("/logout", status_code=204)
def logout_user(token: str = Depends(get_current_token)):
    supabase.auth.sign_out()

    return