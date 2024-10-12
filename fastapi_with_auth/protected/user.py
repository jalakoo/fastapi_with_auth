from fastapi import APIRouter, Depends
from ..auth_config import get_current_user
import logging

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/settings")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """
    Protected route that requires user authentication.
    This route can only be accessed by authenticated users. It logs the access and returns a greeting message.
    Args:
        current_user (dict): The current authenticated user, provided by the dependency injection of `get_current_user`.
    Returns:
        dict: A dictionary containing a greeting message for the authenticated user.
    """

    logging.info(f"Accessed protected user settings for: {current_user}")
    return {"message": f"Hello, {current_user}! This is a protected route."}
