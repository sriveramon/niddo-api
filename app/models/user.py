from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    condoId: int

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
