from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from .auth_config import auth_service
from .models import UserCreate, UserSignIn, ForgotPassword

from .public import access
from .protected import user
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Public routes
app.include_router(access.router)

# Protected routes
app.include_router(user.router)


# Oauth2 Route required for auth via Swagger /docs
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
    token = await auth_service().sign_in(
        {
            "email": form_data.username,
            "password": form_data.password,
        }
    )
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return JSONResponse({"access_token": token, "token_type": "bearer"})


# Public
@app.get("/")
async def root():
    return {"message": "Server running"}



if __name__ == "__main__":
    logger.info("Starting the FastAPI application")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
