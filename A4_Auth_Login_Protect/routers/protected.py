from fastapi import APIRouter, Depends

from dependencies import get_current_user

router = APIRouter(tags=["Protected & Public"])


@router.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


@router.get("/protected/profile")
def protected_profile(
    user=Depends(get_current_user)
):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@router.get("/protected/dashboard")
def protected_dashboard(
    user=Depends(get_current_user)
):
    return {
        "message": "Welcome to your dashboard.",
        "user_id": user.id,
        "email": user.email
    }