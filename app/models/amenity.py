from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base  # Assuming this is your declarative base

class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # ForeignKey to the Condo table
    condo_id = Column(Integer, ForeignKey('condos.id'), nullable=False)

    # Relationship to Condo (this allows you to access the condo from an amenity instance)
    condo = relationship("Condo", back_populates="amenities")  # This needs to match the reverse relationship in Condo model
    reservations = relationship("Reservation", back_populates="amenity", cascade="all, delete-orphan")