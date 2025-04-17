from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.db import Base

class Condo(Base):
    __tablename__ = "condos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=True)

    # Define the reverse relationship to Amenity
    amenities = relationship("Amenity", back_populates="condo", cascade="all, delete-orphan")
    users = relationship("User", back_populates="condo")