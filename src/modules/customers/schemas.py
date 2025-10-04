import json
from pydantic import BaseModel,EmailStr, model_validator # type: ignore
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
    
class AddCustomer(BaseModel):
    name:str
    email:str
    address:str

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        print("Raw value received in validator:", value)
        if isinstance(value, str):
            parsed = json.loads(value)
            print(" After json.loads:", parsed)
            return cls(**parsed)  
        return value