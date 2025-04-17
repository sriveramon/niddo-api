from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    condo_id = Column(Integer, ForeignKey('condos.id'), nullable=False)  # ForeignKey to Condo
    unit = Column(String(50), nullable=False)

    # Relationship to Condo
    condo = relationship("Condo", back_populates="users")
    reservations = relationship("Reservation", back_populates="user")
