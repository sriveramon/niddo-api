from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    condo_id: int

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
