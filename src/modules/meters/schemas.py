import json
from pydantic import BaseModel, model_validator
from typing import Optional

class MeterDetails(BaseModel):
    meter_serial:str
    customer_id:int
    location:str
    installation_year:int
    is_active:bool

    @model_validator(mode="before")
    def validate_to_json(cls, value):
        print("Raw value received in validator:", value)
        if isinstance(value, str):
            parsed = json.loads(value)
            print(" After json.loads:", parsed)
            return cls(**parsed)  
        return value
    

class GetMeter(BaseModel):
    page:Optional[int] = 1
    size: Optional[int] = 10