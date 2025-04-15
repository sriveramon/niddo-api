from typing import Optional  # Import Optional from typing
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException  # Importing HTTPException from FastAPI

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    condoId: int
    unit: Optional[str] = None
    
    @field_validator("email")
    def validate_email(cls, value):
        if "@" not in value:
            raise HTTPException(status_code=400, detail="Invalid email format")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        return value

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    name: str
    email: EmailStr
    unit: Optional[str] = None  # Optional field for unit

    class Config:
        orm_mode = True  # To tell Pydantic to treat ORM models as dictionaries
        
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    condoId: Optional[int] = None
    unit: Optional[str] = None

    @field_validator("email")
    def validate_email(cls, value):
        if "@" not in value:
            raise HTTPException(status_code=400, detail="Invalid email format")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        return value

    class Config:
        orm_mode = True
