from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from .auth_config import get_auth_service
from pydantic import BaseModel
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
security = OAuth2PasswordBearer(tokenUrl="get_token")

auth_service = get_auth_service()


class UserCreate(BaseModel):
    password: str
    email: str


class UserSignIn(BaseModel):
    email: str
    password: str


class ForgotPassword(BaseModel):
    email: str


# Oauth2 Route
@app.post("/get_token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Handles user login and token generation.

    This endpoint receives user credentials via an OAuth2 password request form,
    authenticates the user, and returns a JWT token if the credentials are valid.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the user's email and password.

    Returns:
        JSONResponse: A JSON response containing the access token and token type if authentication is successful.

    Raises:
        HTTPException: If the credentials are invalid, a 400 status code is returned with an error message.
    """
    token = await auth_service.sign_in(
        {
            "email": form_data.username,
            "password": form_data.password,
        }
    )
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return JSONResponse({"access_token": token, "token_type": "bearer"})


async def get_current_user(credentials: Annotated[dict, Depends(security)]):
    logging.info(f"Getting current user with credentials: {credentials}")

    user = await auth_service.get_current_user(credentials)
    if user is None:
        logging.warning(f"Authentication failed")
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    logging.info(f"Authentication successful")
    return user


# Public
@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/signup")
async def signup(user: UserCreate):
    result = await auth_service.sign_up(user.model_dump())
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create user")
    return {"message": "User created successfully"}


@app.post("/forgot-password")
async def forgot_password(data: ForgotPassword):
    result = await auth_service.initiate_password_reset(data.email)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to initiate password reset")
    return {
        "message": "Password reset initiated. Check your email for further instructions."
    }


# Protected
@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """
    Protected route that requires user authentication.
    This route can only be accessed by authenticated users. It logs the access and returns a greeting message.
    Args:
        current_user (dict): The current authenticated user, provided by the dependency injection of `get_current_user`.
    Returns:
        dict: A dictionary containing a greeting message for the authenticated user.
    """

    logging.info(f"Accessed protected route for user: {current_user}")
    return {"message": f"Hello, {current_user}! This is a protected route."}


if __name__ == "__main__":
    logger.info("Starting the FastAPI application")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
