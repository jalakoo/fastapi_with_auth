from .auth_modules.firebase_auth_module import FirebaseAuthModule
from fastapi import Depends, HTTPException, Body
from fastapi.security import (
    OAuth2PasswordBearer,
)
from dotenv import load_dotenv
from typing import Annotated
import logging
import os

# Load environment variables from .env file
load_dotenv()

# Choose the authentication service
AUTH_SERVICE = os.getenv("AUTH_SERVICE", "firebase")

AUTH_CONFIG = {
    "firebase": {
        "api_key": os.getenv("FIREBASE_API_KEY"),
        "auth_domain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "storage_bucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messaging_sender_id": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "app_id": os.getenv("FIREBASE_APP_ID"),
    },
}

current_auth_service = None
current_security = None

def auth_service():
    global current_auth_service
    if current_auth_service is None:
        current_auth_service = _get_auth_service()
    return current_auth_service

def security():
    global current_security
    if current_security is None:
        current_security = _get_security()
    return current_security

def _get_auth_service():
    if AUTH_SERVICE == "firebase":
        return FirebaseAuthModule()
    else:
        raise ValueError(f"Unknown authentication service: {AUTH_SERVICE}")

def _get_security():
    if AUTH_SERVICE == "firebase":
        return OAuth2PasswordBearer(tokenUrl="get_token")
    else:
        raise ValueError(f"Unknown authentication service: {AUTH_SERVICE}")

async def get_current_user(credentials: Annotated[dict, Depends(_get_security())]):
    logging.info(f"Getting current user with credentials: {credentials}")

    user = await auth_service().get_current_user(credentials)
    if user is None:
        logging.warning(f"Authentication failed")
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    logging.info(f"Authentication successful")
    return user