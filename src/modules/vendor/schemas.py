from pydantic import BaseModel
from typing import Optional
class UserBase(BaseModel):
    name: str
    email: str
    address: Optional[str]

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
