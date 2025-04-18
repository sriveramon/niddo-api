from typing import Optional
from pydantic import BaseModel
from datetime import date, time

class BlockCreate(BaseModel):
    amenity_id: int
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    reason: Optional[str] = None

class BlockOut(BaseModel):
    amenity_name: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    reason: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class BlockUpdate(BaseModel):
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    reason: Optional[str] = None
