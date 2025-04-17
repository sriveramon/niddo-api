

from typing import Optional  # Import Optional from typing
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException  # Importing HTTPException from FastAPI

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
