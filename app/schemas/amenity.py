from typing import Optional  # Import Optional from typing
from pydantic import BaseModel
from fastapi import HTTPException  # Importing HTTPException from FastAPI
from datetime import time
class AmenityCreate(BaseModel):
    name: str
    description: str
    start_time: time
    end_time: time
    condo_id: int
    

    class Config:
        orm_mode = True

class AmenityOut(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str

    class Config:
        orm_mode = True  # To tell Pydantic to treat ORM models as dictionaries
        
class AmenityUpdate(BaseModel):
    name: str
    description: str
    start_time: time
    end_time: time
    condo_id: int
    

    class Config:
        orm_mode = True
