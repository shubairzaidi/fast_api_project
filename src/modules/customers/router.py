import shutil
from typing import Annotated, Optional
from fastapi import APIRouter, Depends,File,Form,UploadFile # type: ignore
from sqlalchemy.orm import Session # type: ignore
from src.database.session import get_db
from src.modules.customers import schemas,crud
from src.dependencies.dependencies import get_current_user
from src.database import models
import pandas as pd # type: ignore
from io import BytesIO
from src.utils.helper import custom_http_response
from pathlib import Path
UPLOAD_DIR = Path("src/uploads")
UPLOAD_DIR.mkdir(exist_ok=True) 


router = APIRouter()
""
"Author:Shubair Zaidi"
"Date:27 Sept 2025",
"Purpose: To create Customers"
""
@router.post("/create-customer")
def create_customers(schema_dict:schemas.CustomerDetails,db:Session = Depends(get_db),  current_user: models.User = Depends(get_current_user),):
    return crud.createCustomers(schema_dict,db,current_user)


""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To get Customers"
""
@router.post("/get-customer")
def get_customers(payload:schemas.GetCustomer,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.getCustomers(db,payload)

""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To get Specific Customer"
""
@router.post("/get-customer-by-id/{customer_id}")
def get_customer_by_id(customer_id:Optional[int],db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.getCustomerById(db,customer_id)

""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To delete Customer"
""
@router.post("/delete-customer/{customer_id}")
def delete_customer(customer_id:Optional[int],db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.deleteCustomer(db,customer_id)


""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To update Customer"
""
@router.post("/update-customer/{customer_id}")
def update_customer(payload:schemas.UpdateCustomer,customer_id,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.updateCustomer(db,payload,customer_id)

""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: Download customer list"
""
@router.post("/download")
def download_customer_Excel(db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.downloadCustomerExcel(db)

# to get and convert user information into dict...
def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To add customer using Form"
""
@router.post("/add-customers")
def add_customer_using_form(
    db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    name: str = Form(...),
    email:str = Form(...),
    address:str= Form(),
    profile_photo : UploadFile = File(...)
    ):

    if not name or not email:
        return custom_http_response(
            status_code=200,
            success=False,
            message="Invalid name or email"
        )
    if not profile_photo:
          return custom_http_response(
            status_code=200,
            success=False,
            message="Profile photo is required"
        )
    
    # Save file to server
    file_path = UPLOAD_DIR / profile_photo.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(profile_photo.file, buffer)
    request = {
        "name": name,
        "email": email,
        "address": address,
        "profile_photo": str(file_path) 
    }
    return crud.addCustomer(db,request,current_user)
