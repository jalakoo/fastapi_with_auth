from fastapi import APIRouter, HTTPException
from ..models import UserCreate, UserSignIn, ForgotPassword
from ..auth_config import auth_service

router = APIRouter(
    prefix="/access",
    tags=["access"],
    responses={404: {"description": "Not found"}},
)

@router.post("/signup")
async def signup(user: UserCreate):
    result = await auth_service().sign_up(user.model_dump())
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create user")
    return {"message": "User created successfully"}


@router.post("/forgot-password")
async def forgot_password(data: ForgotPassword):
    result = await auth_service().forgot_password(data.email)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to initiate password reset")
    return {
        "message": "Password reset initiated. Check your email for further instructions."
    }