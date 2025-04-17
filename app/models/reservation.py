from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.db import Base  # Assuming this is your declarative base


class ReservationStatusEnum(str, enum.Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    canceled = 'canceled'
    rejected ='rejected'

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amenity_id = Column(Integer, ForeignKey("amenities.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(ReservationStatusEnum), default=ReservationStatusEnum.pending)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="reservations")
    amenity = relationship("Amenity", back_populates="reservations")