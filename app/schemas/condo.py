from pydantic import BaseModel

class CondoCreate(BaseModel):
    name: str
    address: str
    model_config = {
        "from_attributes": True
    }

class CondoOut(BaseModel):
    name: str
    address: str
    model_config = {
        "from_attributes": True
    }
class CondoUpdate(BaseModel):
    name: str
    address: str
    model_config = {
        "from_attributes": True
    }