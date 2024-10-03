from .auth_modules.firebase_auth_module import FirebaseAuthModule
from dotenv import load_dotenv
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
    # "auth0": {
    #     "domain": os.getenv("AUTH0_DOMAIN"),
    #     "api_audience": os.getenv("AUTH0_API_AUDIENCE"),
    #     "issuer": os.getenv("AUTH0_ISSUER"),
    #     "algorithms": os.getenv("AUTH0_ALGORITHMS", "RS256").split(","),
    # },
}


def get_auth_service():
    if AUTH_SERVICE == "firebase":
        return FirebaseAuthModule()
    else:
        raise ValueError(f"Unknown authentication service: {AUTH_SERVICE}")
