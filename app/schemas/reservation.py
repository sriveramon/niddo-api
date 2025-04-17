from pydantic import BaseModel
from datetime import time, date
from enum import Enum

class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"
    rejected = "rejected"
    
class ReservationCreate(BaseModel):
    user_id: int
    amenity_id: str
    date: date
    start_time: time
    end_time: time
    status: ReservationStatus    # Assuming you have a predefined enum for status
    

    class Config:
        from_attributes = True

class ReservationOut(BaseModel):
    user_name: str
    amenity_name: str
    date: date
    start_time: time
    end_time: time
    status: str    # Assuming you have a predefined enum for status

    class Config:
        from_attributes = True
        
class ReservationUpdate(BaseModel):
    user_id: int
    amenity_id: str
    date: date
    start_time: time
    end_time: time
    status: ReservationStatus    # Assuming you have a predefined enum for status
    

    class Config:
        from_attributes = True
