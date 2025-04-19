from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.db.db import Base  # Adjust import path to your project structure
import enum

class VisitorStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    identification = Column(String(100), nullable=True)
    visit_name = Column(String(length=100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    condo_id = Column(Integer, ForeignKey("condos.id"), nullable=False)
    plate = Column(String(20), nullable=True)
    visit_date = Column(Date, nullable=False)
    status = Column(Enum(VisitorStatus), default=VisitorStatus.pending, nullable=False)
    unit_number = Column(String(50), nullable=False)  # Added unit_number
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    # Optional relationships
    user = relationship("User", back_populates="visitors")
    condo = relationship("Condo", back_populates="visitors")
