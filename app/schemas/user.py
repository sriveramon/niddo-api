from typing import Optional  # Import Optional from typing
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException  # Importing HTTPException from FastAPI

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    condo_id: int
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
    
class UserOut(BaseModel):
    name: str
    email: EmailStr
    unit: Optional[str] = None  # Optional field for unit
    model_config = {
        "from_attributes": True
    }
   
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    condo_id: Optional[int] = None
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
