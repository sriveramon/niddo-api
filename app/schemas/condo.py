from pydantic import BaseModel

class CondoCreate(BaseModel):
    name: str
    address: str

    class Config:
        orm_mode = True

class CondoOut(BaseModel):
    name: str
    address: str
    
    class Config:
        orm_mode = True  # To tell Pydantic to treat ORM models as dictionaries
        
class CondoUpdate(BaseModel):
    name: str
    address: str

    class Config:
        orm_mode = True
