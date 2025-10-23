from typing import Optional
from pydantic import BaseModel, EmailStr


class CreateContractor(BaseModel):
    contractor_name:str
    contact_phone:Optional[str]
    license_number:Optional[str]
    contact_email:Optional[EmailStr]
    address:Optional[str]

    