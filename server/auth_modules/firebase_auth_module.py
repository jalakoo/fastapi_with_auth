from .base_auth_module import BaseAuthModule
from firebase_admin import credentials, auth, initialize_app
from fastapi import HTTPException
import os
import requests
import logging


class FirebaseAuthModule(BaseAuthModule):
    def __init__(self):
        self.api_key = os.getenv("FIREBASE_API_KEY")
        cred = credentials.Certificate(
            {
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
            }
        )
        initialize_app(cred)

    async def sign_in(self, user_data: dict):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"

        payload = {
            "email": user_data.get("email"),
            "password": user_data.get("password"),
            "returnSecureToken": True,
        }

        response = requests.post(url, json=payload)

        logging.info(f"Reponse: {response.json()}")

        if response.status_code == 200:
            id_token = response.json().get("idToken")
            return id_token
        else:
            print(f"Error: {response.json()}")
            return None

    async def get_current_user(self, credentials: dict | str):
        logging.info(
            f"firebase auth module: get_current_user: credentials: {credentials}"
        )
        token = credentials
        if isinstance(credentials, dict):
            token = credentials.get("idToken")
        elif isinstance(credentials, str):
            token = credentials
        else:
            return HTTPException(
                401, detail="Credentials must be a dictionary or string"
            )

        if not token:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        try:
            decoded_token = auth.verify_id_token(token)
            return {
                "uid": decoded_token["uid"],
                "email": decoded_token.get("email"),
                "name": decoded_token.get("name"),
            }
        except:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

    async def sign_up(self, user_data: dict) -> bool:
        try:
            auth.create_user(
                email=user_data.get("email"),
                password=user_data.get("password"),
                display_name=user_data.get("username"),
            )
            return True
        except:
            return False

    async def delete_user(self, user_id: str) -> bool:
        try:
            auth.delete_user(user_id)
            return True
        except:
            return False

    async def forgot_password(self, email: str) -> bool:
        try:
            auth.generate_password_reset_link(email)
            return True
        except:
            return False
