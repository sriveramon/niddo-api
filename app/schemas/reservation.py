from typing import Optional  # Import Optional from typing
from pydantic import BaseModel
from fastapi import HTTPException  # Importing HTTPException from FastAPI
from datetime import time, date
from enum import Enum

class ReservationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    
class ReservationCreate(BaseModel):
    user_id: int
    amenity_id: str
    date: date
    start_time: time
    end_time: time
    status: ReservationStatus    # Assuming you have a predefined enum for status
    

    class Config:
        orm_mode = True

class ReservationOut(BaseModel):
    user_name: str
    amenity_name: str
    date: str
    start_time: str
    end_time: str
    status: str    # Assuming you have a predefined enum for status

    class Config:
        orm_mode = True  # To tell Pydantic to treat ORM models as dictionaries
        
class ReservationUpdate(BaseModel):
    user_id: int
    amenity_id: str
    date: date
    start_time: time
    end_time: time
    satus: ReservationStatus    # Assuming you have a predefined enum for status
    

    class Config:
        orm_mode = True
