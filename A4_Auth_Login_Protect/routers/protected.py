from fastapi import APIRouter, HTTPException, Header

router = APIRouter(tags=["Protected and Public"])


@router.get("/public/info")
def public_info():
    return {
        "message": "Welcome! You are accessing public info"
    }


@router.get("/protected/profile")
def protected_profile(
    authorization: str | None = Header(default=None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Access token required."
        )

    token = authorization.split(" ", 1)[1]

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Access token required."
        )

    return {
        "message": "Token Accessed."
    }