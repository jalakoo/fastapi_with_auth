from pydantic import BaseModel

class UserCreate(BaseModel):
    password: str
    email: str


class UserSignIn(BaseModel):
    email: str
    password: str


class ForgotPassword(BaseModel):
    email: str