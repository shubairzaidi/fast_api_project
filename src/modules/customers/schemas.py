from pydantic import BaseModel,EmailStr # type: ignore
from typing import Optional

class CustomerDetails(BaseModel):
    name:str
    address:str
    email:EmailStr

class GetCustomer(BaseModel):
    page:Optional[int] = 1
    size:Optional[int] = 10

class UpdateCustomer(BaseModel):
    name:str
    email:str
    address:Optional[str]
    