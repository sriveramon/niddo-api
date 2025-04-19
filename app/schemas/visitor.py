from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class VisitorStatus(str, Enum):
    pending = "pending"
    approved = "approved"

class VisitorCreate(BaseModel):
    identification: Optional[str] = None  # Made identification optional (nullable)
    user_id: int
    visit_name: str
    condo_id: int
    plate: Optional[str] = None  # Made plate optional (nullable)
    visit_date: date
    status: VisitorStatus = VisitorStatus.pending
    unit_number: str  # Added unit_number

    class Config:
        from_attributes = True

class VisitorOut(BaseModel):
    id: int
    identification: Optional[str] = None  # Made identification optional (nullable)
    visit_name: str
    user_id: int
    condo_id: int
    plate: Optional[str] = None  # Made plate optional (nullable)
    visit_date: date
    status: VisitorStatus
    unit_number: str  # Added unit_number

    class Config:
        from_attributes = True

class VisitorUpdate(BaseModel):
    identification: Optional[str] = None  # Made identification optional (nullable)
    visit_name: str
    plate: Optional[str] = None  # Made plate optional (nullable)
    visit_date: date
    status: VisitorStatus
    unit_number: str  # Added unit_number

    class Config:
        from_attributes = True
