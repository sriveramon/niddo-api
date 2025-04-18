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
    
class AmenityOut(BaseModel):
    id: int
    name: str
    description: str
    start_time: time
    end_time: time
    
    model_config = {
        "from_attributes": True
    }

class AmenityUpdate(BaseModel):
    name: str
    description: str
    start_time: time
    end_time: time
    condo_id: int
    
