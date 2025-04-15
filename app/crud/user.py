from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.hash import bcrypt

def create_user(db: Session, user: UserCreate):
    hashed_pw = bcrypt.hash(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()
