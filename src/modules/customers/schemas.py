from pydantic import BaseModel,EmailStr
from typing import Optional

class CustomerDetails(BaseModel):
    name:str
    address:str
    email:EmailStr

