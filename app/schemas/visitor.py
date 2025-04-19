from pydantic import BaseModel
from datetime import date
from enum import Enum

class VisitorStatus(str, Enum):
    pending = "pending"
    approved = "approved"

class VisitorCreate(BaseModel):
    identification: str
    user_id: int
    visit_name: str
    condo_id: int
    plate: str | None = None
    visit_date: date
    status: VisitorStatus = VisitorStatus.pending
    unit_number: str  # Added unit_number

    class Config:
        from_attributes = True

class VisitorOut(BaseModel):
    id: int
    identification: str
    visit_name: str
    user_id: int
    condo_id: int
    plate: str | None = None
    visit_date: date
    status: VisitorStatus
    unit_number: str  # Added unit_number

    class Config:
        from_attributes = True

class VisitorUpdate(BaseModel):
    identification: str
    visit_name: str
    plate: str | None = None
    visit_date: date
    status: VisitorStatus
    unit_number: str  # Added unit_number

    class Config:
        from_attributes = True
