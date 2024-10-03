# FastAPI Authentication Service

This project is a FastAPI-based authentication service that supports multiple authentication methods.

## Prerequisites

- Python 3.7+
- Poetry (Python dependency management tool)

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Running the Application

1. Make sure you're in the project root directory.

2. Activate the Poetry shell + run the FastAPI server:

   ```
   poetry shell
   uvicorn fastapi_with_auth.main:app --reload
   ```

   or together like:

   ```
   poetry run uvicorn fastapi_with_auth.main:app --reload --log-level info
   ```

3. The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /`: Root endpoint, returns a welcome message.
- `GET /protected`: Protected route, requires authentication.
- `POST /signup`: Create a new user account.
- `POST /signin`: Authenticate a user.
- `POST /forgot-password`: Initiate the password reset process.

For detailed API documentation, visit `http://127.0.0.1:8000/docs` after starting the server.

## Testing

You can use tools like curl, Postman, or the built-in Swagger UI (`/docs`) to test the API endpoints.

## Development

To change the authentication service:

1. Modify the AUTH_SERVICE var in the `.env` file in the root directory or directly when starting the server:

```
AUTH_SERVICE=basic
```

Current options: - basic - firebase - auth0

2. Ensure you have the necessary dependencies and configurations for the chosen authentication service.

3. Restart the FastAPI server for the changes to take effect.

Remember to update any environment variables or additional configuration files that may be required for the chosen authentication service.

To add new dependencies:

```
poetry add <dependency>
```
