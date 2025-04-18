# models/block.py
from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.db import Base  # Assuming this is your declarative base

class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    amenity_id = Column(Integer, ForeignKey("amenities.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
   
   # Relationship
    amenity = relationship("Amenity", back_populates="blocks")