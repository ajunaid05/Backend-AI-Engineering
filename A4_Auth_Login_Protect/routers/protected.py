from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database import supabase

router = APIRouter(tags=["Protected & Public"])
security = HTTPBearer()

@router.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


@router.get("/protected/profile")
def protected_profile(
    credentials : HTTPAuthorizationCredentials = Depends(security)
):

    

    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

    except Exception as e:
        print("Supabase verification error:", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired token."
        )

    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired token."
        )

    user = response.user

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }